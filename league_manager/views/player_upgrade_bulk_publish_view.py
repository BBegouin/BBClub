__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import UpdateAPIView
from league_manager.models.ref_skills import Ref_Skills
from rest_framework.response import Response
from league_manager.models.player_upgrade import PlayerUpgrade
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer

class PlayerUpgradeBulkPublishView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = UpgradeSerializer

    """
     Permet de publier plusieurs upgrade de joueurs
    """
    def patch(self, request, *args, **kwargs):

        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas publier d'upgrade de joueur")

        # un admin peut publier n'importe quel upgrade de joueur
        if  user.is_superuser is False :
            # on vérifie que les upgrade portent tous sur des joueurs appartenant à l'utilisateur connecté
            for up_data in request.data:
                if 'id' not in up_data:
                    raise NotAcceptable("L'id d'un des upgrades est manquant")

                up = PlayerUpgrade.objects.get(pk=up_data['id'])
                if up.player.team.user != user:
                    raise NotAcceptable("Il est interdit de publier une upgrade sur les joueurs d'un autre coach !")

                up.publish(up_data)


        serializer = UpgradeSerializer(up)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")