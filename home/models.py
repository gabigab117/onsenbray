from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from core.models import BasePage


class HomePage(BasePage):
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Je vais ajouter des variables contextuelles ici si nécessaire
        return context
