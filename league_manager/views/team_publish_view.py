__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from league_manager.models.team import Team
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.team_serializers import TeamSerializer

class TeamPublishView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = TeamSerializer

    """
     un appel patch sur l'id d'une team draft permet de la publier
    """
    def patch(self, request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['pk'])
        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas publier une équipe")

        # si l'utilisateur est loggué mais que la team ne lui appartient pas et qu'il n'est pas admin
        # on refuse la publication
        if team.user != user and user.is_superuser is False :
            raise NotAcceptable("La publication d'une équipe externe interdite")

        # si on est arrivé là, la publication peut se faire
        team.status = 1
        team.save()
        serializer = TeamSerializer(team)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")