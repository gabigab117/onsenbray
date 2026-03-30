import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.documents.models import Document
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage
from ordinance.models import Ordinance, OrdinanceIndexPage

User = get_user_model()


class OrdinanceModelTests(TestCase):
    """
    Feature: Gestion des arrêtés
        En tant qu'administrateur
        Je veux gérer les arrêtés municipaux et préfectoraux
        Afin de les rendre disponibles aux citoyens
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="author@example.com", password="testpass123"
        )
        cls.document = Document.objects.create(title="Arrêté test")
        cls.ordinance = Ordinance.objects.create(
            title="Arrêté de voirie",
            date=datetime.date(2026, 3, 10),
            document=cls.document,
            author=cls.user,
            type=Ordinance.Type.MUNICIPAL,
        )

    def test_type_choices(self):
        """
        Scenario: Les types d'arrêtés disponibles
            Given le modèle Ordinance
            When je vérifie les choix de type
            Then "municipal" et "prefectural" sont disponibles
        """
        choices = [c[0] for c in Ordinance.Type.choices]
        self.assertIn("municipal", choices)
        self.assertIn("prefectural", choices)

    def test_ordering(self):
        """
        Scenario: Les arrêtés sont ordonnés par date décroissante
            Given deux arrêtés avec des dates différentes
            When je récupère la liste des arrêtés
            Then le plus récent apparaît en premier
        """
        doc2 = Document.objects.create(title="Arrêté 2")
        older = Ordinance.objects.create(
            title="Ancien arrêté",
            date=datetime.date(2026, 1, 5),
            document=doc2,
            author=self.user,
            type=Ordinance.Type.PREFECTORAL,
        )
        ordinances = list(Ordinance.objects.all())
        self.assertEqual(ordinances[0], self.ordinance)
        self.assertEqual(ordinances[1], older)

    def test_author_set_null_on_delete(self):
        """
        Scenario: Suppression de l'auteur d'un arrêté
            Given un arrêté avec un auteur
            When l'auteur est supprimé
            Then le champ auteur de l'arrêté devient null
        """
        user = User.objects.create_user(
            email="temp@example.com", password="testpass123"
        )
        doc = Document.objects.create(title="Arrêté temp")
        ordinance = Ordinance.objects.create(
            title="Arrêté temporaire",
            date=datetime.date(2026, 2, 1),
            document=doc,
            author=user,
        )
        user.delete()
        ordinance.refresh_from_db()
        self.assertIsNone(ordinance.author)


class OrdinanceIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index des arrêtés
        En tant que visiteur
        Je veux consulter la liste des arrêtés
        Afin de prendre connaissance des décisions administratives
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
        cls.index = OrdinanceIndexPage(
            title="Arrêtés", slug="arretes", body="Liste des arrêtés"
        )
        cls.home.add_child(instance=cls.index)

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'index des arrêtés
            Given une page index d'arrêtés publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_ordinances(self):
        """
        Scenario: Le contexte contient les arrêtés paginés
            Given une page index d'arrêtés
            When un visiteur accède à la page
            Then le contexte contient la clé "ordinances"
        """
        response = self.client.get(self.index.url)
        self.assertIn("ordinances", response.context)
