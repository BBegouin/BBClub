__author__ = 'Bertrand'

from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from league_manager.models.player import Player
from django.http import Http404
from league_manager.views.serializers.team_serializers import TeamSerializer

from league_manager.views.serializers.team_serializers import PlayerSerializer,CreatePlayerSerializer
from league_manager.views.serializers.skill_serializer import DetailedSkillSerializer,SkillSerializer
from rest_framework.response import Response

class GeneralRanking(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GeneralRankingSerializer
    queryset = Player.objects.all()
