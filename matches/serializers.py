from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            "id",
            "tournament",
            "player1",
            "player2",
            "result",
            "round",
        )
