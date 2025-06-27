from django.db import models
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


User = get_user_model()


class SchoolIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        menus = CanteenMenu.objects.all().order_by('-date')
        
        paginator = Paginator(menus, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['menus'] = page_obj
        return context


class CanteenMenu(models.Model):
    date = models.DateField("Date du menu")
    document = models.ForeignKey(
        'wagtaildocs.Document',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Menu de la cantine",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='canteen_menus',
        verbose_name="Auteur",
        null=True
    )
    
    class Meta:
        verbose_name = "Menu de la cantine"
        verbose_name_plural = "Menus de la cantine"
        ordering = ['-date']
    
    def __str__(self):
        return f"Menu du {self.date.strftime('%d/%m/%Y')}"
