__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from league_manager.models.match_report import MatchReport
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated,NotAcceptable
from league_manager.views.serializers.match_report_serializer import MatchReportSerializer

class MatchReportPublishView(UpdateAPIView):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    serializer_class = MatchReportSerializer

    """
     un appel patch sur l'id d'un rapport de match draft permet de le publier.
    """
    def patch(self, request, *args, **kwargs):
        match = MatchReport.objects.get(pk=kwargs['pk'])
        user = request.user
        if type(user) is AnonymousUser:
            raise NotAuthenticated("un utilisateur anonyme ne peut pas publier rapport de match")

        # un admin peut publier n'importe quel rapport de match
        if  user.is_superuser is False :
            # un utilisateur ne peut publier qu'un rapport de match qui concerne une de ses équipe
            if match.team_reports.team[0].user != user and match.team_reports.team[1].user != user:
                raise NotAcceptable("Il est interdit de publier un rapport externe")

        # si on est arrivé là, la publication peut se faire
        match.publish()
        match.save()

        serializer = MatchReportSerializer(match)

        return Response(serializer.data)

    """
     On implémente cette méthode définie par le mixin afin d'être sûr qu'elle ne soit pas utilisée
    """
    def put(self, request, *args, **kwargs):
        raise NotAcceptable("méthode non supportée")