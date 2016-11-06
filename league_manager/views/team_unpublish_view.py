__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from league_manager.models.team import Team
from league_manager.models.team_report import TeamReport
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.team_serializers import TeamSerializer

class TeamUnPublishView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = TeamSerializer

    """
     un appel patch sur l'id d'un team draft permet de la dépublier
    """
    def patch(self, request, *args, **kwargs):
        team = Team.objects.get(pk=kwargs['pk'])
        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas dépublier une équipe")

        # si l'utilisateur est loggué mais que la team ne lui appartient pas et qu'il n'est pas admin
        # on refuse la publication
        if team.user != user and user.is_superuser is False :
            raise NotAcceptable("La dépublication d'une équipe externe interdite")

        #on ne peut dépublier une équipe que si elle n'a pas encore joué, donc si elle n'a pas de rapport de match
        match_count = TeamReport.objects.filter(team=team).count()
        if match_count != 0:
            raise NotAcceptable("Il est impossible de dépublier une équipe qui a déjà joué")

        # si on est arrivé là, la dépublication peut se faire
        team.status = 0
        team.save()
        serializer = TeamSerializer(team)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")