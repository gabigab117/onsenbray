import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.documents.models import Document
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage
from school.models import CanteenMenu, SchoolIndexPage

User = get_user_model()


class CanteenMenuModelTests(TestCase):
    """
    Feature: Gestion des menus de cantine
        En tant qu'administrateur
        Je veux gérer les menus de la cantine scolaire
        Afin de les rendre disponibles aux parents
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="author@example.com", password="testpass123"
        )
        cls.document = Document.objects.create(title="Menu semaine 12")
        cls.menu = CanteenMenu.objects.create(
            date=datetime.date(2026, 3, 16),
            end_date=datetime.date(2026, 3, 20),
            document=cls.document,
            author=cls.user,
        )

    def test_ordering(self):
        """
        Scenario: Les menus sont ordonnés par date décroissante
            Given deux menus avec des dates différentes
            When je récupère la liste des menus
            Then le plus récent apparaît en premier
        """
        doc2 = Document.objects.create(title="Menu ancien")
        older = CanteenMenu.objects.create(
            date=datetime.date(2026, 1, 6),
            end_date=datetime.date(2026, 1, 10),
            document=doc2,
            author=self.user,
        )
        menus = list(CanteenMenu.objects.all())
        self.assertEqual(menus[0], self.menu)
        self.assertEqual(menus[1], older)

    def test_author_set_null_on_delete(self):
        """
        Scenario: Suppression de l'auteur d'un menu
            Given un menu avec un auteur
            When l'auteur est supprimé
            Then le champ auteur du menu devient null
        """
        user = User.objects.create_user(
            email="temp@example.com", password="testpass123"
        )
        doc = Document.objects.create(title="Menu temp")
        menu = CanteenMenu.objects.create(
            date=datetime.date(2026, 2, 2),
            end_date=datetime.date(2026, 2, 6),
            document=doc,
            author=user,
        )
        user.delete()
        menu.refresh_from_db()
        self.assertIsNone(menu.author)


class SchoolIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index de l'école
        En tant que visiteur
        Je veux consulter la page de l'école
        Afin d'accéder aux menus de la cantine
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
        cls.index = SchoolIndexPage(
            title="École", slug="ecole", body="Informations scolaires"
        )
        cls.home.add_child(instance=cls.index)

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'index de l'école
            Given une page index de l'école publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_menus(self):
        """
        Scenario: Le contexte contient les menus paginés
            Given une page index de l'école
            When un visiteur accède à la page
            Then le contexte contient la clé "menus"
        """
        response = self.client.get(self.index.url)
        self.assertIn("menus", response.context)
