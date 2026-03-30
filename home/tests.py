import datetime

from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from event.models import EventIndexPage, EventPage, Organizer
from home.models import HomePage


class HomePageTests(WagtailPageTestCase):
    """
    Feature: Page d'accueil
        En tant que visiteur
        Je veux accéder à la page d'accueil
        Afin de voir les dernières actualités et événements
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

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'accueil
            Given une page d'accueil publiée
            When un visiteur accède à la racine du site
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_last_event_and_news(self):
        """
        Scenario: Le contexte contient le dernier événement et la dernière actualité
            Given une page d'accueil, un événement et une actualité
            When un visiteur accède à la page d'accueil
            Then le contexte contient "last_event" et "last_news"
        """
        response = self.client.get(self.home.url)
        self.assertIn("last_event", response.context)
        self.assertIn("last_news", response.context)

    def test_context_last_event_is_most_recent(self):
        """
        Scenario: Le dernier événement est le plus récent
            Given deux événements avec des dates différentes
            When un visiteur accède à la page d'accueil
            Then "last_event" correspond à l'événement le plus récent
        """
        event_index = EventIndexPage(
            title="Événements", slug="evenements", body="Events"
        )
        self.home.add_child(instance=event_index)
        organizer = Organizer.objects.create(name="Mairie")

        old_event = EventPage(
            title="Ancien",
            slug="ancien",
            date=timezone.make_aware(datetime.datetime(2026, 1, 1, 10, 0)),
            localisation="Place",
            organizer=organizer,
            body=[],
        )
        event_index.add_child(instance=old_event)

        recent = EventPage(
            title="Récent",
            slug="recent",
            date=timezone.make_aware(datetime.datetime(2026, 6, 1, 10, 0)),
            localisation="Salle",
            organizer=organizer,
            body=[],
        )
        event_index.add_child(instance=recent)

        response = self.client.get(self.home.url)
        self.assertEqual(response.context["last_event"], recent)
