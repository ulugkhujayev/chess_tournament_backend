from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Match
from tournaments.models import Tournament
from datetime import date

User = get_user_model()


class MatchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user1 = User.objects.create_user(
            "player1", "player1@test.com", "player1pass"
        )
        self.user2 = User.objects.create_user(
            "player2", "player2@test.com", "player2pass"
        )
        self.tournament = Tournament.objects.create(
            name="Test Tournament",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 7),
        )

    def test_create_match(self):
        data = {
            "tournament": self.tournament.id,
            "player1": self.user1.id,
            "player2": self.user2.id,
            "round": 1,
        }
        response = self.client.post("/api/matches/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)
        self.assertEqual(Match.objects.get().player1, self.user1)

    def test_record_result(self):
        match = Match.objects.create(
            tournament=self.tournament, player1=self.user1, player2=self.user2, round=1
        )
        data = {"result": "1-0"}
        response = self.client.patch(f"/api/matches/{match.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        match.refresh_from_db()
        self.assertEqual(match.result, "1-0")

    def test_list_matches(self):
        Match.objects.create(
            tournament=self.tournament, player1=self.user1, player2=self.user2, round=1
        )
        response = self.client.get("/api/matches/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_match(self):
        match = Match.objects.create(
            tournament=self.tournament, player1=self.user1, player2=self.user2, round=1
        )
        response = self.client.delete(f"/api/matches/{match.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 0)
