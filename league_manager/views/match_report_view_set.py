__author__ = 'Bertrand'

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from core.permissions.admin_delete import AdminDeleteOnly
from league_manager.models.match_report import MatchReport
from league_manager.views.serializers.match_report_serializer import MatchReportSerializer,CreateMatchReportSerializer,UpdateMatchReportSerializer

class MatchReportViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminDeleteOnly,)
    queryset = MatchReport.objects.all()

    def get_queryset(self):
        """
        on filtre selon l'équipe, afin de connaître les matchs joués
        """
        team = self.request.query_params.get('team', None)
        if team is not None:
            queryset = MatchReport.objects.filter(team_reports__team=team)
        else:
            queryset = MatchReport.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve' \
            or self.action == 'destroy':
                return MatchReportSerializer
        elif self.action == 'update'\
            or self.action == 'partial_update':
            return UpdateMatchReportSerializer
        elif self.action == 'create':
            return CreateMatchReportSerializer
