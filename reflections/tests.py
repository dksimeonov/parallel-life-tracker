from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from parallel_lives.models import LifeDomain, ParallelLife
from reflections.models import ReflectionEntry

User = get_user_model()


class ReflectionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email = "owner@example.com",
            password = "StrongPass123!"
        )
        self.other_user = User.objects.create_user(
            username="other",
            email = "other@example.com",
            password = "StrongPass123!"
        )
        self.domain = LifeDomain.objects.create(name = "Travel")
        self.life = ParallelLife.objects.create(
            owner = self.user,
            title = "What if I had moved to Japan",
            divergence_date = "2024-03-01",
            starting_choice = "I moved abroad after university",
            summary = "An alternate life focused on language, traver and cultural adaptation.",
            visibility = "public",
            status = "draft",
            realism_score = 8,
        )
        self.life.domains.add(self.domain)
        self.reflection = ReflectionEntry.objects.create(
            user = self.user,
            parallel_life = self.life,
            title = "First Reflection",
            content = "This path feels difficult but exciting and deeply transformative.",
            mood_score= 8,
            is_private= True,
        )

    def test_owner_can_create_reflection(self):
        self.client.login(username="owner", password="StrongPass123!")
        response = self.client.post(reverse("reflection-create", kwargs={"slug":self.life.slug}), {
            "title": "Second Reflection",
            "content": "I am curious how this alternate life would reshape my priorities and mindset.",
            "mood_score": 7,
            "is_private": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ReflectionEntry.objects.filter(title = "Second Reflection").exists())

    def test_non_owner_cannot_create_reflection(self):
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("reflection-create", kwargs={"slug":self.life.slug}))
        self.assertEqual(response.status_code, 403)

    def test_private_reflection_hidden_from_other_user(self):
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("parallel-life-detail", kwargs={"slug":self.life.slug}))
        self.assertNotContains(response, "First Reflection")
