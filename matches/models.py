from django.db import models
from tournaments.models import Tournament
from django.contrib.auth import get_user_model

User = get_user_model()


class Match(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="matches"
    )
    player1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="matches_as_player1"
    )
    player2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="matches_as_player2"
    )
    result = models.CharField(
        max_length=10,
        choices=[
            ("1-0", "Player 1 Wins"),
            ("0-1", "Player 2 Wins"),
            ("1/2-1/2", "Draw"),
        ],
        null=True,
        blank=True,
    )
    round = models.IntegerField()

    def __str__(self):
        return (
            f"{self.player1.username} vs {self.player2.username} - Round {self.round}"
        )
