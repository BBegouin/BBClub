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

class PlayerUpgradePublishView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = UpgradeSerializer

    """
     un appel patch sur l'id d'un rapport de match draft permet de le publier.
    """
    def patch(self, request, *args, **kwargs):

        up = PlayerUpgrade.objects.get(pk=kwargs['pk'])

        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas publier d'upgrade de joueur")

        # un admin peut publier n'importe quel upgrade de joueur
        if  user.is_superuser is False :
            # un utilisateur ne peut publier qu'un upgrade sur l'un de ses joueur
            if up.player.team.user != user:
                raise NotAcceptable("Il est interdit de publier une upgrade sur les joueurs d'un autre coach !")

        up.value = request.data['value']

        #NB : on ne met pas à jour le statut, en cas de boulette dans les données
        if request.data['value'] == 0 or request.data['value'] == 1:
            up.skill = Ref_Skills.objects.get(pk=request.data['skill'])

        # si on a une maj de skill, il faut vérifier
        up.publish()

        serializer = UpgradeSerializer(up)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")