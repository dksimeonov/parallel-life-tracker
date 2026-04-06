from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from parallel_lives.models import LifeDomain, ParallelLife

User = get_user_model()


class ParallelLifeApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "apiuser",
            email = "api@example.com",
            password = "StrongPass123!"
        )
        self.other_user = User.objects.create_user(
            username = "other",
            email = "other@example.com",
            password = "StrongPass123!"
        )
        self.domain = LifeDomain.objects.create(name = "Career")

        self.public_life = ParallelLife.objects.create(
            owner = self.user,
            title = "Public API Life",
            divergence_date = "2024-01-01",
            starting_choice = "A different career decision",
            summary = "This public life is used for API endpoint testing purposes.",
            visibility = "public",
            status = "draft",
            realism_score = 7,
        )
        self.public_life.domains.add(self.domain)

        self.private_life = ParallelLife.objects.create(
            owner = self.user,
            title = "Private API Life",
            divergence_date = "2024-01-02",
            starting_choice = "A secret personal decision",
            summary = "This private life is not visible to anonymous API users.",
            visibility = "private",
            status = "draft",
            realism_score = 6,
        )
        self.private_life.domains.add(self.domain)

    def test_api_list_shows_public_lives_for_anonymous(self):
        response = self.client.get("/api/parallel-lives/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Public API Life")

    def test_api_detail_shows_public_life(self):
        response = self.client.get(f"/api/parallel-lives/{self.public_life.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Public API Life")

    def test_api_detail_shows_private_life_from_anonymous(self):
        response = self.client.get(f"/api/parallel-lives/{self.private_life.id}/")
        self.assertEqual(response.status_code, 404)
