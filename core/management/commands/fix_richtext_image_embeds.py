"""
Management command to find and fix rich text fields containing image embeds
without an 'id' attribute, which causes KeyError: 'id' in Wagtail's
reference extraction (extract_references_from_rich_text).
"""

import re

from django.core.management.base import BaseCommand
from django.db import transaction

# Pattern for image embeds missing the id attribute
BROKEN_IMAGE_EMBED_RE = re.compile(
    r'<embed[^>]*embedtype=["\']image["\'][^>]*(?<!id=)[^>]*/?>',
    re.IGNORECASE,
)

# More precise: match embed tags with embedtype=image but no id= attribute
EMBED_TAG_RE = re.compile(r'<embed\b[^>]*/>', re.IGNORECASE)

HAS_EMBEDTYPE_IMAGE = re.compile(r'embedtype=["\']image["\']', re.IGNORECASE)
HAS_ID_ATTR = re.compile(r'\bid=["\'][^"\']+["\']', re.IGNORECASE)


def find_broken_embeds(html):
    """Return all image embed tags that are missing an id attribute."""
    broken = []
    for tag in EMBED_TAG_RE.findall(html):
        if HAS_EMBEDTYPE_IMAGE.search(tag) and not HAS_ID_ATTR.search(tag):
            broken.append(tag)
    return broken


def remove_broken_embeds(html):
    """Remove image embed tags missing an id attribute from the html string."""
    def replace_tag(m):
        tag = m.group(0)
        if HAS_EMBEDTYPE_IMAGE.search(tag) and not HAS_ID_ATTR.search(tag):
            return ''
        return tag

    return EMBED_TAG_RE.sub(replace_tag, html)


class Command(BaseCommand):
    help = (
        "Find (and optionally fix) rich text fields containing image embeds "
        "without an 'id' attribute (causes KeyError: 'id' in Wagtail)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Remove the broken embed tags from the database (default: dry-run)',
        )

    def handle(self, *args, **options):
        fix = options['fix']
        found_any = False

        # Collect (model, instance, field_name, broken_tags) tuples
        targets = self._collect_rich_text_fields()

        for model, pk, field_name, value in targets:
            if not value:
                continue
            broken = find_broken_embeds(value)
            if not broken:
                continue

            found_any = True
            label = f"{model.__name__} pk={pk} field='{field_name}'"
            self.stdout.write(self.style.WARNING(f"[BROKEN] {label}"))
            for tag in broken:
                self.stdout.write(f"         {tag}")

            if fix:
                cleaned = remove_broken_embeds(value)
                with transaction.atomic():
                    model.objects.filter(pk=pk).update(**{field_name: cleaned})
                self.stdout.write(self.style.SUCCESS(f"         → Fixed and saved."))

        if not found_any:
            self.stdout.write(self.style.SUCCESS("No broken image embeds found."))
        elif not fix:
            self.stdout.write(
                self.style.NOTICE(
                    "\nRun with --fix to remove the broken embed tags from the database."
                )
            )

    def _collect_rich_text_fields(self):
        """
        Yield (model_class, pk, field_name, raw_value) tuples.
        Uses raw SQL for StreamFields to bypass the StreamValue descriptor.
        """
        from wagtail.fields import RichTextField, StreamField
        from django.apps import apps
        from django.db import connection

        for model in apps.get_models():
            rich_fields = []
            stream_fields = []

            for field in model._meta.get_fields():
                if isinstance(field, RichTextField):
                    rich_fields.append(field.name)
                elif isinstance(field, StreamField):
                    stream_fields.append(field.name)

            if not rich_fields and not stream_fields:
                continue

            table = model._meta.db_table
            pk_col = model._meta.pk.column

            # RichTextFields via ORM .values()
            if rich_fields:
                try:
                    for row in model.objects.values(pk_col, *rich_fields).iterator():
                        for fname in rich_fields:
                            value = row.get(fname)
                            if value and isinstance(value, str):
                                yield model, row[pk_col], fname, value
                except Exception:
                    pass

            # StreamFields via raw SQL to avoid from_db_value conversion
            for fname in stream_fields:
                col = model._meta.get_field(fname).column
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f'SELECT "{pk_col}", "{col}" FROM "{table}"'
                            f' WHERE "{col}" IS NOT NULL AND "{col}" != \'\''
                        )
                        for pk, raw_value in cursor.fetchall():
                            if raw_value and isinstance(raw_value, str):
                                yield model, pk, fname, raw_value
                except Exception:
                    pass
