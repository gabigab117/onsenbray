from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


class PhotoComparisonPage(Page):
    body = RichTextField("Contenu introductif", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        comparisons = PhotoComparison.objects.select_related(
            'image_before', 'image_after'
        ).order_by('order')
        
        context['comparisons'] = comparisons
        return context


class PhotoComparison(models.Model):
    """Modèle pour une comparaison avant/après"""
    
    title = models.CharField("Titre", max_length=255)
    description = RichTextField("Description", blank=True)
    
    image_before = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Photo 'Avant'"
    )
    
    image_after = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Photo 'Après'"
    )
    
    order = models.IntegerField("Ordre d'affichage", default=0)
    
    class Meta:
        verbose_name = "Comparaison de photos"
        verbose_name_plural = "Comparaisons de photos"
        ordering = ['order', 'title']
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image_before'),
        FieldPanel('image_after'),
        FieldPanel('order'),
    ]
    
    def __str__(self):
        return self.title