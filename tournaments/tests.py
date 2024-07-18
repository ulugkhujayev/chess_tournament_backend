from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tournament
from datetime import date

User = get_user_model()


class TournamentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user1 = User.objects.create_user(
            "player1", "player1@test.com", "player1pass", rating=1500
        )
        self.user2 = User.objects.create_user(
            "player2", "player2@test.com", "player2pass", rating=1600
        )

    def test_create_tournament(self):
        data = {
            "name": "Test Tournament",
            "start_date": "2023-01-01",
            "end_date": "2023-01-07",
            "participants": [self.user1.id, self.user2.id],
        }
        response = self.client.post("/api/tournaments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(Tournament.objects.get().name, "Test Tournament")

    def test_generate_pairings(self):
        tournament = Tournament.objects.create(
            name="Pairing Test Tournament",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 7),
        )
        tournament.participants.add(self.user1, self.user2)
        pairings = tournament.generate_pairings()
        self.assertEqual(len(pairings), 1)
        self.assertEqual(
            pairings[0], (self.user2, self.user1)
        )  # Higher rated player should be first

    def test_get_standings(self):
        tournament = Tournament.objects.create(
            name="Standings Test Tournament",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 7),
        )
        tournament.participants.add(self.user1, self.user2)
        # Create a match and record a result
        match = tournament.matches.create(
            player1=self.user1, player2=self.user2, round=1, result="1-0"
        )
        standings = tournament.get_standings()
        self.assertEqual(len(standings), 2)
        self.assertEqual(standings[0]["player"], self.user1)
        self.assertEqual(standings[0]["points"], 1)
        self.assertEqual(standings[1]["player"], self.user2)
        self.assertEqual(standings[1]["points"], 0)

    def test_update_tournament(self):
        tournament = Tournament.objects.create(
            name="Update Test Tournament",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 7),
        )
        data = {
            "name": "Updated Tournament",
            "start_date": "2023-02-01",
            "end_date": "2023-02-07",
        }
        response = self.client.patch(f"/api/tournaments/{tournament.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tournament.refresh_from_db()
        self.assertEqual(tournament.name, "Updated Tournament")
        self.assertEqual(str(tournament.start_date), "2023-02-01")

    def test_delete_tournament(self):
        tournament = Tournament.objects.create(
            name="Delete Test Tournament",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 7),
        )
        response = self.client.delete(f"/api/tournaments/{tournament.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tournament.objects.count(), 0)
