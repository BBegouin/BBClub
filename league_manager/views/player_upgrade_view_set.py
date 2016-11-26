__author__ = 'Bertrand'
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer
from league_manager.models.player_upgrade import PlayerUpgrade
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework import viewsets


class PlayerUpgradeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = PlayerUpgrade.objects.all()

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve' :
                return UpgradeSerializer
        elif  self.action == 'update'\
            or  self.action == 'partial_update':
            return UpgradeSerializer
        elif  self.action == 'destroy'\
            or self.action == 'create':
            return None