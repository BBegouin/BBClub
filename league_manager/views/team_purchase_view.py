__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from league_manager.models.team import Team
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.team_serializers import TeamSerializer

class TeamPurchaseView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = TeamSerializer

    """
     un appel patch sur l'id d'une team draft permet de la publier
    """
    def patch(self, request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['pk'])
        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas acheter du stuff pour une équipe")

        # si l'utilisateur est loggué mais que la team ne lui appartient pas et qu'il n'est pas admin
        # on refuse l'achat
        if team.user != user and user.is_superuser is False :
            raise NotAcceptable("Les achats ne peuvent être faits que par le proprio d'une équipe")

        # on vérifie que l'équipe est dans un état compatible d'achat
        if team.status !=1:
            raise NotAcceptable("Les achats sont impossible sur une équipe draft")

        # si on est arrivé là, on peut lancer la publication des achats
        team.publish_purchases(request.data)

        serializer = TeamSerializer(team)

        # on renvoi l'équipe
        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")