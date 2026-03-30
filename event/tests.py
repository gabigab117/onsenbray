import datetime

from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from event.models import EventIndexPage, EventPage, Organizer
from home.models import HomePage


class EventIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index des événements
        En tant que visiteur
        Je veux consulter la liste des événements
        Afin de connaître les activités à venir
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
        cls.index = EventIndexPage(
            title="Événements", slug="evenements", body="Nos événements"
        )
        cls.home.add_child(instance=cls.index)

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'index des événements
            Given une page index d'événements publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)

    def test_allowed_subpage_types(self):
        """
        Scenario: Seules les pages EventPage sont autorisées en sous-page
            Given le type EventIndexPage
            When je vérifie les sous-pages autorisées
            Then seul EventPage est autorisé
        """
        self.assertAllowedSubpageTypes(EventIndexPage, {EventPage})

    def test_context_contains_events(self):
        """
        Scenario: Le contexte contient les événements paginés
            Given une page index d'événements
            When un visiteur accède à la page
            Then le contexte contient la clé "events"
        """
        response = self.client.get(self.index.url)
        self.assertIn("events", response.context)


class EventPageTests(WagtailPageTestCase):
    """
    Feature: Page d'événement
        En tant que visiteur
        Je veux consulter le détail d'un événement
        Afin de connaître les informations pratiques
    """

    @classmethod
    def setUpTestData(cls):
        root = Page.objects.first()
        cls.home = HomePage(title="Accueil", slug="accueil-evt", body="Bienvenue")
        root.add_child(instance=cls.home)
        Site.objects.all().delete()
        Site.objects.create(
            hostname="localhost", root_page=cls.home, is_default_site=True
        )
        cls.index = EventIndexPage(
            title="Événements", slug="evenements", body="Nos événements"
        )
        cls.home.add_child(instance=cls.index)
        cls.organizer = Organizer.objects.create(name="Mairie")
        cls.event = EventPage(
            title="Fête de la musique",
            slug="fete-musique",
            date=timezone.make_aware(datetime.datetime(2026, 6, 21, 18, 0)),
            localisation="Place du village",
            event_type=EventPage.EventType.INTERNAL,
            organizer=cls.organizer,
            body=[],
        )
        cls.index.add_child(instance=cls.event)

    def test_parent_page_type(self):
        """
        Scenario: Un événement ne peut être créé que sous l'index
            Given le type EventPage
            When je vérifie les types de pages parentes autorisés
            Then seul EventIndexPage est autorisé
        """
        self.assertAllowedParentPageTypes(EventPage, {EventIndexPage})

    def test_page_accessible(self):
        """
        Scenario: Accès à une page d'événement
            Given un événement publié
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.event.url)
        self.assertEqual(response.status_code, 200)

    def test_event_type_choices(self):
        """
        Scenario: Les types d'événements disponibles
            Given le modèle EventPage
            When je vérifie les choix de type
            Then "external" et "internal" sont disponibles
        """
        choices = [c[0] for c in EventPage.EventType.choices]
        self.assertIn("external", choices)
        self.assertIn("internal", choices)
