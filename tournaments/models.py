from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(User, related_name="tournaments")
    current_round = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def generate_pairings(self):
        players = list(self.participants.all().order_by("-rating"))
        pairings = []
        while len(players) > 1:
            player1 = players.pop(0)
            player2 = players.pop(0)
            pairings.append((player1, player2))
        return pairings

    def record_result(self, match, result):
        match.result = result
        match.save()
        # Update player ratings here (e.g., using Elo rating system)

    def get_standings(self):
        standings = []
        for player in self.participants.all():
            wins = self.matches.filter(
                Q(player1=player, result="1-0") | Q(player2=player, result="0-1")
            ).count()
            draws = self.matches.filter(
                Q(player1=player) | Q(player2=player), result="1/2-1/2"
            ).count()
            points = wins + 0.5 * draws
            standings.append({"player": player, "points": points})
        return sorted(standings, key=lambda x: x["points"], reverse=True)
