__author__ = 'Bertrand'
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from rest_framework import viewsets
from league_manager.models.team import Team
from league_manager.views.serializers.team_serializers import TeamSerializer,CreateTeamSerializer, TeamUpdateSerializer

class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = Team.objects.all()

    def get_queryset(self):
        """
        on filtre selon l'utilisateur, parametre optionnel de requête get
        """
        coach = self.request.query_params.get('coach', None)
        if coach is not None:
            queryset = Team.objects.filter(user=coach)
        else:
            queryset = Team.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve' \
            or self.action == 'destroy':
                return TeamSerializer
        elif self.action == 'update'\
            or self.action == 'partial_update':
            return TeamUpdateSerializer
        elif self.action == 'create':
            return CreateTeamSerializer
