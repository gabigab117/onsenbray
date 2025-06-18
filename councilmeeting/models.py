from django.db import models
from django.contrib.auth import get_user_model
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.models import register_snippet


User = get_user_model()


class CouncilMeetingIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        meetings = CouncilMeeting.objects.all().order_by('-date')
        context['meetings'] = meetings
        return context


@register_snippet
class CouncilMeeting(models.Model):
    date = models.DateField("Date de la réunion")
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Compte rendu de la réunion",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='council_meetings',
        verbose_name="Auteur",
        null=True
    )

    panels = [
        FieldPanel("date"),
        FieldPanel("document"),
        FieldPanel("author"),
    ]
    
    class Meta:
        verbose_name = "Réunion du conseil municipal"
        verbose_name_plural = "Réunions du conseil municipal"
        ordering = ['-date']
    
    def __str__(self):
        return f"Réunion du {self.date.strftime('%d/%m/%Y')}"
