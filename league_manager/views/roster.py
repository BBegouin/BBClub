__author__ = 'Bertrand'
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from league_manager.models.ref_roster import Ref_Roster
from league_manager.views.serializers.roster_list_serializers import RosterListSerializer

class RosterList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Ref_Roster.objects.all()
    serializer_class = RosterListSerializer
