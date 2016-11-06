__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.player import Player
from league_manager.views.serializers.roster_list_serializers import RosterLineSerializer
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer

class GeneralRankingSerializer(serializers.ModelSerializer):
    ref_roster_line = RosterLineSerializer(many=False,read_only=True)
    evolution = UpgradeSerializer(many=True,read_only=True)
    class Meta:
        model = Player
