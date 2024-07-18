from rest_framework.decorators import action
from rest_framework.response import Response
from chess_tournament.base_views import BaseViewSet
from .models import Tournament
from .serializers import TournamentSerializer
from .tasks import generate_pairings_task


class TournamentViewSet(BaseViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    @action(detail=True, methods=["post"])
    def generate_pairings(self, request, pk=None):
        tournament = self.get_object()
        generate_pairings_task.delay(tournament.id)
        return Response({"message": "Pairings generation task has been queued"})

    @action(detail=True, methods=["post"])
    def record_result(self, request, pk=None):
        tournament = self.get_object()
        match_id = request.data.get("match_id")
        result = request.data.get("result")
        try:
            match = tournament.matches.get(id=match_id)
            tournament.record_result(match, result)
            return Response({"message": "Result recorded successfully"})
        except tournament.matches.model.DoesNotExist:
            return Response(
                {"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def standings(self, request, pk=None):
        tournament = self.get_object()
        standings = tournament.get_standings()
        return Response(standings)
