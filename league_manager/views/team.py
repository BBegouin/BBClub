__author__ = 'Bertrand'
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.models.team import Team
from league_manager.views.serializers.team_serializers import TeamSerializer,CreateTeamSerializer

class TeamCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateTeamSerializer

class TeamList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Team.objects.all()
    serializer_class = CreateTeamSerializer
