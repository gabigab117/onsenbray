from django.test import TestCase
from wagtail.models import Page, Site

from home.models import HomePage


class SearchViewTests(TestCase):
    """
    Feature: Recherche globale
        En tant que visiteur
        Je veux effectuer une recherche sur le site
        Afin de trouver rapidement l'information souhaitée
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

    def test_search_page_accessible(self):
        """
        Scenario: Accès à la page de recherche
            Given le site est en ligne
            When un visiteur accède à /search/
            Then la page est servie avec un code 200
        """
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_search_with_query(self):
        """
        Scenario: Recherche avec un terme
            Given le site est en ligne
            When un visiteur recherche "accueil"
            Then la page de résultats est servie avec un code 200
            And le contexte contient la requête et les résultats
        """
        response = self.client.get("/search/", {"query": "accueil"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_query"], "accueil")
        self.assertIn("search_results", response.context)

    def test_search_without_query(self):
        """
        Scenario: Recherche sans terme
            Given le site est en ligne
            When un visiteur accède à /search/ sans paramètre
            Then la page est servie avec un code 200
            And les résultats sont vides
        """
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["search_results"]), 0)
