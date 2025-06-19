from django.db import models
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


User = get_user_model()


class OrdinanceIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        ordinances = Ordinance.objects.all().order_by('-date')

        paginator = Paginator(ordinances, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['ordinances'] = page_obj  # C'est un objet Page, pas une liste
        return context


class Ordinance(models.Model):
    
    class Type(models.TextChoices):
        MUNICIPAL = 'municipal', 'Municipal'
        PREFECTORAL = 'prefectural', 'Préfectoral'
    
    date = models.DateField("Date de l'arrêté")
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Arrêté",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='ordinances',
        verbose_name="Auteur",
        null=True
    )
    type = models.CharField(
        "Type d'arrêté",
        max_length=20,
        choices=Type,
        default=Type.MUNICIPAL,
    )
    
    class Meta:
        verbose_name = "Arrêté"
        verbose_name_plural = "Arrêtés"
        ordering = ['-date']
    
    def __str__(self):
        return f"Arrêté du {self.date.strftime('%d/%m/%Y')}"
