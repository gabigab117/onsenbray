from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class CustomUserManagerTests(TestCase):
    """
    Feature: Gestion des utilisateurs personnalisés
        En tant qu'administrateur
        Je veux créer des utilisateurs avec un email comme identifiant
        Afin de simplifier l'authentification
    """

    def test_create_user(self):
        """
        Scenario: Création d'un utilisateur standard
            Given un email "user@example.com" et un mot de passe "testpass123"
            When je crée un utilisateur avec ces identifiants
            Then l'utilisateur est créé avec l'email normalisé
            And l'utilisateur n'est ni staff ni superuser
        """
        user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises(self):
        """
        Scenario: Tentative de création d'un utilisateur sans email
            Given un email vide
            When je tente de créer un utilisateur
            Then une ValueError est levée
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

    def test_create_superuser(self):
        """
        Scenario: Création d'un superutilisateur
            Given un email "admin@example.com" et un mot de passe "adminpass123"
            When je crée un superutilisateur
            Then l'utilisateur est staff et superuser
        """
        admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_not_staff_raises(self):
        """
        Scenario: Tentative de création d'un superutilisateur sans is_staff
            Given is_staff=False
            When je tente de créer un superutilisateur
            Then une ValueError est levée
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="adminpass123", is_staff=False
            )

    def test_create_superuser_not_superuser_raises(self):
        """
        Scenario: Tentative de création d'un superutilisateur sans is_superuser
            Given is_superuser=False
            When je tente de créer un superutilisateur
            Then une ValueError est levée
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="adminpass123", is_superuser=False
            )

    def test_email_is_normalized(self):
        """
        Scenario: Normalisation de l'email
            Given un email "user@EXAMPLE.COM"
            When je crée un utilisateur
            Then le domaine de l'email est en minuscules
        """
        user = User.objects.create_user(
            email="user@EXAMPLE.COM", password="testpass123"
        )
        self.assertEqual(user.email, "user@example.com")

    def test_username_field_is_email(self):
        """
        Scenario: Le champ d'identification est l'email
            Given le modèle CustomUser
            When je vérifie le USERNAME_FIELD
            Then c'est "email"
        """
        self.assertEqual(User.USERNAME_FIELD, "email")
