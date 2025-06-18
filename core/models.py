from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField


class BasePage(Page):
    body = RichTextField()
    
    class Meta:
        abstract = True


class StandardPage(BasePage):
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    subpage_types = list()
