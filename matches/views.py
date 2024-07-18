from chess_tournament.base_views import BaseViewSet
from .models import Match
from .serializers import MatchSerializer


class MatchViewSet(BaseViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
