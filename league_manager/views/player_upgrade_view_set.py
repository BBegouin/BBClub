__author__ = 'Bertrand'
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer,CreateUpgradeSerializer
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.team import Team
from django.http import HttpResponseForbidden
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework import viewsets


class PlayerUpgradeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = Team.objects.all()

    def get_queryset(self):
        """
        on filtre selon l'utilisateur, parametre optionnel de requête get
        """
        player = self.request.query_params.get('player', None)
        if player is not None:
            queryset = Team.objects.filter(user=player)
        else:
            queryset = Team.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve' :
                return UpgradeSerializer
        elif self.action == 'create':
            return CreateUpgradeSerializer
        elif  self.action == 'destroy'\
            or self.action == 'update'\
            or self.action == 'partial_update':
            return None