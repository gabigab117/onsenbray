from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.search import index


class AssociationIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    max_count = 1

    subpage_types = ['association.AssociationPage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        associations = AssociationPage.objects.live().order_by('title')
        context['associations'] = associations
        return context


class AssociationPage(Page):
    summary = RichTextField("Résumé", max_length=255, help_text="Bref résumé de l'association")
    body = StreamField([
        ('text', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
    ]
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('summary'),
    ]

    parent_page_types = ['association.AssociationIndexPage']
