__author__ = 'Bertrand'
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.models.player import Player
from league_manager.models.player_evolution import PlayerEvolution
from league_manager.models.ref_skills import Ref_Skills
from django.http import Http404
from league_manager.views.serializers.team_serializers import TeamSerializer

from league_manager.views.serializers.team_serializers import PlayerSerializer
from league_manager.views.serializers.skill_serializer import DetailedSkillSerializer,SkillSerializer
from rest_framework.response import Response

class PlayerList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

class PlayerDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

class PlayerTeam(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TeamSerializer

    def get_object(self, pk):
        try:
            return Player.objects.get(pk=pk).team
        except Player.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

class PlayerAdditionalSkills(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DetailedSkillSerializer

    def get_queryset(self):
        player_pk = self.kwargs['pk']
        skills = Ref_Skills.objects.filter(playerevolution__player = player_pk)

        return skills