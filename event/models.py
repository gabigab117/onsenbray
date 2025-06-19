from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import StreamField
from wagtail.search import index
from django.core.paginator import Paginator


class EventIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    subpage_types = ['event.EventPage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        events = EventPage.objects.live().order_by('-date')

        paginator = Paginator(events, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['events'] = page_obj
        return context


class EventPage(Page):

    class EventType(models.TextChoices):
        EXTERNAL = 'external', 'Externe'
        INTERNAL = 'internal', 'Interne'

    event_type = models.CharField(
        "Type d'événement",
        max_length=20,
        choices=EventType,
        default=EventType.INTERNAL,
    )
    date = models.DateTimeField("Date de l'événement")
    localisation = models.CharField("Localisation", max_length=255)
    body = StreamField([
        ('text', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
    ], use_json_field=True, blank=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("localisation"),
        FieldPanel("body"),
        FieldPanel("event_type"),
    ]
    
    parent_page_types = ['event.EventIndexPage']
