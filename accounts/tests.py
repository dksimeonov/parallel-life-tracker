from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile

User = get_user_model()


class AccountsTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "display_name": "New User",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_profile_created_after_user_registration(self):
        self.client.post(reverse("register"), {
            "username": "profileuser",
            "email": "profileuser@example.com",
            "display_name": "Profile User",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        user = User.objects.get(username="profileuser")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_user_can_login(self):
        user = User.objects.create_user(
            username="loginuser",
            email= "login@example.com",
            password= "StrongPass123!",
        )
        response = self.client.post(reverse("login"), {
            "username": "loginuser",
            "password": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_open_dashboard(self):
        user = User.objects.create_user(
            username="dashuser",
            email= "dash@example.com",
            password= "StrongPass123!",
        )
        self.client.login(username= "dashuser", password= "StrongPass123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_page_requires_login(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertEqual(response.status_code, 302)











