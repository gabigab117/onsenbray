from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from core.models import BasePage
from event.models import EventPage
from news.models import NewsPage


class HomePage(BasePage):
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    max_count = 1
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        last_event = EventPage.objects.order_by('-date').first()
        context['last_event'] = last_event
        last_news = NewsPage.objects.order_by('-date').first()
        context['last_news'] = last_news
        return context
