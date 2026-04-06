from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from parallel_lives.models import LifeDomain, ParallelLife

User = get_user_model()


class ParallelLifeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "owner",
            email = "owner@example.com",
            password = "StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username = "other",
            email = "other@example.com",
            password = "StrongPass123!"
        )
        self.domain = LifeDomain.objects.create(name = "Career")
        self.life = ParallelLife.objects.create(
            owner = self.user,
            title = "What if I had become a designer",
            divergence_date = "2024-01-01",
            starting_choice = "I chose design over programming",
            summary = "A completely different professional path with creative challenges.",
            visibility = "public",
            status = "draft",
            realism_score= 7,
        )
        self.life.domains.add(self.domain)

    def test_parallel_life_list_page_loads(self):
        response = self.client.get(reverse("parallel-lives-list"))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_create_parallel_life(self):
        self.client.login(username="owner", password="StrongPass123!")
        response = self.client.post(reverse("parallel-life-create"), {
            "title": "What if I had moved abroad",
            "divergence_date": "2024-02-01",
            "starting_choice": "I accepted an offer abroad",
            "summary": "This alternate life explores adaptation, work and identity in another country.",
            "visibility": "public",
            "status": "draft",
            "realism_score": 8,
            "domains": [self.domain.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ParallelLife.objects.filter(title = "What if I had moved abroad").exists())

    def test_owner_can_edit_own_parallel_life(self):
        self.client.login(username="owner", password="StrongPass123!")
        response = self.client.post(
            reverse("parallel-life-edit", kwargs={"slug": self.life.slug}),
            {
                "title": "Updated Life Title",
                "divergence_date": "2024-01-01",
                "starting_choice": "I chose design over programming",
                "summary": "A completely different professional path with creative challenges.",
                "visibility": "public",
                "status": "draft",
                "realism_score": "7",
                "domains": [str(self.domain.pk)],
            },
            follow = False,
        )
        self.assertEqual(response.status_code, 302)
        self.life.refresh_from_db()
        self.assertEqual(self.life.title, "Updated Life Title")

    def test_non_owner_cannot_edit_parallel_life(self):
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("parallel-life-edit", kwargs = {"slug":self.life.slug}))
        self.assertEqual(response.status_code, 403)

    def test_private_parallel_life_not_visible_to_other_user(self):
        self.life.visibility = "private"
        self.life.save()
        self.client.login(username="other", password="StrongPass123!")
        response = self.client.get(reverse("parallel-life-detail", kwargs = {"slug":self.life.slug}))
        self.assertEqual(response.status_code, 404)
