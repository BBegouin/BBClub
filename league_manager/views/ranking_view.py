__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from league_manager.models.player import Player
from rest_framework.response import Response
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.ref_skills import Ref_Skills
from league_manager.models.team import Team
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer
from django.core.exceptions import ObjectDoesNotExist
from league_manager.views.serializers.ranking_line_serializer import RankingLineSerializer
from league_manager.models.ranking_line import RankingLine
from rest_framework import viewsets

class RankingView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RankingLineSerializer

    """
     Récupération des équipes et initialisation de la liste des objets ranking line
    """
    def get_queryset(self):
        user = self.request.user
        # dans l'absolu il faudrait récupérer les équipes inscrite à une ligue, pour l'instant
        # on récupére tout
        team_list = Team.objects.all().order_by('-ranking_points', '-bonus_point')
        ranking_line = []
        for team in team_list:
            ranking_line.append(RankingLine(team))

        #on retourne la liste d'objet ranking line
        return ranking_line
