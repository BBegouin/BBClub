__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.player import Player
from league_manager.views.serializers.roster_list_serializers import RosterLineSerializer
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer

class PlayerSerializer(serializers.ModelSerializer):
    ref_roster_line = RosterLineSerializer(many=False,read_only=True)
    evolution = UpgradeSerializer(many=True,read_only=True)
    class Meta:
        model = Player

class CreatePlayerSerializer(serializers.ModelSerializer):
    miss_next_game = serializers.BooleanField(default=False)
    need_upgrade = serializers.BooleanField(default=False)
    total_xp = serializers.IntegerField(default=0)

    class Meta:
        model = Player
        fields=('name','ref_roster_line','num','miss_next_game','need_upgrade','total_xp')

class UpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields=('name','miss_next_game','num','total_xp')
