from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from association.models import AssociationIndexPage, AssociationPage
from home.models import HomePage


class AssociationIndexPageTests(WagtailPageTestCase):
    """
    Feature: Page d'index des associations
        En tant que visiteur
        Je veux voir la liste des associations
        Afin de découvrir les associations de la commune
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
        cls.index = AssociationIndexPage(
            title="Associations", slug="associations", body="Liste des associations"
        )
        cls.home.add_child(instance=cls.index)

    def test_can_create_under_home(self):
        """
        Scenario: Création d'une page index sous la page d'accueil
            Given une page d'accueil existante
            When je crée une page AssociationIndexPage
            Then la page est créée avec succès
        """
        self.assertCanCreateAt(HomePage, AssociationIndexPage)

    def test_association_page_as_child(self):
        """
        Scenario: Ajout d'une association sous la page index
            Given une page index d'associations
            When je crée une AssociationPage en sous-page
            Then la page est créée avec succès
        """
        self.assertAllowedSubpageTypes(
            AssociationIndexPage, {AssociationPage}
        )

    def test_index_page_accessible(self):
        """
        Scenario: Accès à la page d'index des associations
            Given une page index d'associations publiée
            When un visiteur accède à l'URL de la page
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.index.url)
        self.assertEqual(response.status_code, 200)


class AssociationPageTests(WagtailPageTestCase):
    """
    Feature: Page d'association
        En tant que visiteur
        Je veux consulter les détails d'une association
        Afin de connaître ses activités
    """

    @classmethod
    def setUpTestData(cls):
        root = Page.objects.first()
        cls.home = HomePage(title="Accueil", slug="accueil-assoc", body="Bienvenue")
        root.add_child(instance=cls.home)
        Site.objects.all().delete()
        Site.objects.create(
            hostname="localhost", root_page=cls.home, is_default_site=True
        )
        cls.index = AssociationIndexPage(
            title="Associations", slug="associations", body="Liste"
        )
        cls.home.add_child(instance=cls.index)
        cls.page = AssociationPage(
            title="Club de sport",
            slug="club-sport",
            summary="Résumé du club",
            body=[],
        )
        cls.index.add_child(instance=cls.page)

    def test_parent_page_type(self):
        """
        Scenario: Une association ne peut être créée que sous l'index
            Given le type AssociationPage
            When je vérifie les types de pages parentes autorisés
            Then seul AssociationIndexPage est autorisé
        """
        self.assertAllowedParentPageTypes(
            AssociationPage, {AssociationIndexPage}
        )

    def test_page_accessible(self):
        """
        Scenario: Accès à la page d'une association
            Given une page d'association publiée
            When un visiteur accède à l'URL
            Then la page est servie avec un code 200
        """
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
