from chess_tournament.base_views import BaseViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
