from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from milestones.models import Milestone
from parallel_lives.models import LifeDomain, ParallelLife

User = get_user_model()


class MilestoneTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "owner",
            email = "owner@example.com",
            password = "StrongPass123!"
        )
        self.domain = LifeDomain.objects.create(name = "Career")
        self.life = ParallelLife.objects.create(
            owner = self.user,
            title = "What if I had become a musician",
            divergence_date = "2024-01-01",
            starting_choice = "I followed music full-time",
            summary = "A life path focused on art, discipline and performance challenges.",
            visibility = "public",
            status = "draft",
            realism_score= 6,
        )
        self.life.domains.add(self.domain)
        self.milestone = Milestone.objects.create(
            parallel_life = self.life,
            title = "Record first album",
            description = "Finish and record the first professional album.",
            status = "planned",
            progress = 10,
            created_by = self.user,
        )

    def test_owner_can_view_milestone_list(self):
        self.client.login(username = "owner", password = "StrongPass123!")
        response = self.client.get(reverse("milestone-list", kwargs={"slug":self.life.slug}))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_view_milestone_list(self):
        self.client.login(username = "other", password = "StrongPass123!")
        response = self.client.get(reverse("milestone-list", kwargs={"slug":self.life.slug}))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_create_milestone(self):
        self.client.login(username = "owner", password = "StrongPass123!")
        response = self.client.post(reverse("milestone-create", kwargs={"slug":self.life.slug}), {
            "title": "Find a producer",
            "description": "Connect with a producer and plan the studio process.",
            "target_date": "2026-01-01",
            "status": "in_progress",
            "progress": 20,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Milestone.objects.filter(title="Find a producer").exists())
