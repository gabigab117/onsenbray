import datetime

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage
from news.models import NewsIndexPage, NewsPage


class NewsIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index des actualités
        En tant que visiteur
        Je veux consulter la liste des actualités
        Afin de suivre les nouvelles de la commune
    """

    @classmethod
    def setUpTestData(cls):
        root = Page.objects.first()
        cls.home = HomePage(title="Accueil", slug="accueil", body="Bienvenue")
        root.add_child(instance=cls.home)
        Site.objects.all().delete()
        Site.objects.create(
            hostname="localhost", root_page=cls.home, is_default_site=True
        )
        cls.index = NewsIndexPage(
            title="Actualités", slug="actualites", body="Nos actualités"
        )
        cls.home.add_child(instance=cls.index)

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'index des actualités
            Given une page index d'actualités publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_allowed_subpage_types(self):
        """
        Scenario: Seules les pages NewsPage sont autorisées en sous-page
            Given le type NewsIndexPage
            When je vérifie les sous-pages autorisées
            Then seul NewsPage est autorisé
        """
        self.assertAllowedSubpageTypes(NewsIndexPage, {NewsPage})

    def test_context_contains_news_items(self):
        """
        Scenario: Le contexte contient les actualités paginées
            Given une page index d'actualités
            When un visiteur accède à la page
            Then le contexte contient la clé "news_items"
        """
        response = self.client.get(self.index.url)
        self.assertIn("news_items", response.context)


class NewsPageTests(WagtailPageTestCase):
    """
    Feature: Page d'actualité
        En tant que visiteur
        Je veux consulter le détail d'une actualité
        Afin de lire les nouvelles
    """

    @classmethod
    def setUpTestData(cls):
        root = Page.objects.first()
        cls.home = HomePage(title="Accueil", slug="accueil-news", body="Bienvenue")
        root.add_child(instance=cls.home)
        Site.objects.all().delete()
        Site.objects.create(
            hostname="localhost", root_page=cls.home, is_default_site=True
        )
        cls.index = NewsIndexPage(
            title="Actualités", slug="actualites", body="Nos actualités"
        )
        cls.home.add_child(instance=cls.index)
        cls.page = NewsPage(
            title="Nouvelle route",
            slug="nouvelle-route",
            date=datetime.date(2026, 3, 1),
            body=[],
        )
        cls.index.add_child(instance=cls.page)

    def test_parent_page_type(self):
        """
        Scenario: Une actualité ne peut être créée que sous l'index
            Given le type NewsPage
            When je vérifie les types de pages parentes autorisés
            Then seul NewsIndexPage est autorisé
        """
        self.assertAllowedParentPageTypes(NewsPage, {NewsIndexPage})

    def test_page_accessible(self):
        """
        Scenario: Accès à une page d'actualité
            Given une actualité publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
