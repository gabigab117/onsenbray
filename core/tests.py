from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from core.models import StandardPage
from home.models import HomePage


class StandardPageTests(WagtailPageTestCase):
    """
    Feature: Page standard
        En tant qu'administrateur
        Je veux créer des pages de contenu simple
        Afin de publier des informations générales
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
        cls.page = StandardPage(
            title="Mentions légales", slug="mentions-legales", body="<p>Contenu</p>"
        )
        cls.home.add_child(instance=cls.page)

    def test_no_subpages_allowed(self):
        """
        Scenario: Une page standard ne peut pas avoir de sous-pages
            Given le type StandardPage
            When je vérifie les types de sous-pages autorisés
            Then aucun type n'est autorisé
        """
        self.assertAllowedSubpageTypes(StandardPage, set())

    def test_page_accessible(self):
        """
        Scenario: Accès à une page standard
            Given une page standard publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
