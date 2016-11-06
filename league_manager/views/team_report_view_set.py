__author__ = 'Bertrand'

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from core.permissions.delete_forbidden import DeleteForbidden
from league_manager.models.team_report import TeamReport
from league_manager.views.serializers.team_report_serializer import TeamReportSerializer,CreateStandaloneTeamReportSerializer,UpdateTeamReportSerializer

class TeamReportViewSet(viewsets.ModelViewSet):
    permission_classes = (DeleteForbidden,)
    queryset = TeamReport.objects.all()

    def get_queryset(self):
        """
        on filtre selon l'équipe, afin de connaître les rapports de match de l'équipe joués
        """
        team = self.request.query_params.get('team', None)
        if team is not None:
            queryset = TeamReport.objects.filter(team=team)
        else:
            queryset = TeamReport.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve':
                return TeamReportSerializer
        elif self.action == 'update'\
            or self.action == 'partial_update':
            return UpdateTeamReportSerializer
        elif self.action == 'create':
            return CreateStandaloneTeamReportSerializer
        elif self.action == 'destroy':
            return None
