import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from wagtail.documents.models import Document
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from councilmeeting.models import CouncilMeeting, CouncilMeetingIndexPage
from home.models import HomePage

User = get_user_model()


class CouncilMeetingModelTests(TestCase):
    """
    Feature: Gestion des comptes rendus de réunions du conseil
        En tant qu'administrateur
        Je veux gérer les comptes rendus de réunion
        Afin de les rendre disponibles aux citoyens
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="author@example.com", password="testpass123"
        )
        cls.document = Document.objects.create(title="CR Réunion")
        cls.meeting = CouncilMeeting.objects.create(
            date=datetime.date(2026, 3, 15),
            document=cls.document,
            author=cls.user,
        )

    def test_ordering(self):
        """
        Scenario: Les réunions sont ordonnées par date décroissante
            Given deux réunions avec des dates différentes
            When je récupère la liste des réunions
            Then la plus récente apparaît en premier
        """
        doc2 = Document.objects.create(title="CR Réunion 2")
        older = CouncilMeeting.objects.create(
            date=datetime.date(2026, 1, 10),
            document=doc2,
            author=self.user,
        )
        meetings = list(CouncilMeeting.objects.all())
        self.assertEqual(meetings[0], self.meeting)
        self.assertEqual(meetings[1], older)

    def test_author_set_null_on_delete(self):
        """
        Scenario: Suppression de l'auteur d'une réunion
            Given une réunion avec un auteur
            When l'auteur est supprimé
            Then le champ auteur de la réunion devient null
        """
        user = User.objects.create_user(
            email="temp@example.com", password="testpass123"
        )
        doc = Document.objects.create(title="CR Temp")
        meeting = CouncilMeeting.objects.create(
            date=datetime.date(2026, 2, 1), document=doc, author=user
        )
        user.delete()
        meeting.refresh_from_db()
        self.assertIsNone(meeting.author)


class CouncilMeetingIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index des réunions du conseil
        En tant que visiteur
        Je veux consulter la liste des comptes rendus
        Afin de suivre les décisions du conseil
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
        cls.index = CouncilMeetingIndexPage(
            title="Conseil municipal", slug="conseil", body="Comptes rendus"
        )
        cls.home.add_child(instance=cls.index)

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'index du conseil
            Given une page index du conseil publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_meetings(self):
        """
        Scenario: Le contexte contient les réunions paginées
            Given une page index du conseil
            When un visiteur accède à la page
            Then le contexte contient la clé "meetings"
        """
        response = self.client.get(self.index.url)
        self.assertIn("meetings", response.context)
