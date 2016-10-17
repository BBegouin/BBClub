__author__ = 'Bertrand'
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.models.team import Team
from league_manager.views.serializers.team_serializers import TeamSerializer,CreateTeamSerializer
from rest_framework.response import Response
from django.http import Http404


class TeamCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateTeamSerializer

class TeamList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TeamSerializer(snippet)
        return Response(serializer.data)
