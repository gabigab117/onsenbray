from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import RichTextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class CouncilMeetingIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    subpage_types = ["councilmeeting.CouncilMeetingPage"]
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        meetings = CouncilMeetingPage.objects.child_of(self).live().order_by('-date')
        context['meetings'] = meetings
        return context


class CouncilMeetingPage(Page):
    date = models.DateField("Date de la réunion")
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Compte rendu de la réunion",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("document"),
    ]
    
    parent_page_types = ["councilmeeting.CouncilMeetingIndexPage"]
    subpage_types = []
