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


class NewsIndexPage(Page):
    body = RichTextField("Contenu")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    
    max_count = 1
    
    subpage_types = ['news.NewsPage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        news_items = NewsPage.objects.live().order_by('-date')

        paginator = Paginator(news_items, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['news_items'] = page_obj
        return context


class NewsPage(Page):
    date = models.DateField("Date de publication")
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
        FieldPanel("body"),
    ]
    
    parent_page_types = ['news.NewsIndexPage']
