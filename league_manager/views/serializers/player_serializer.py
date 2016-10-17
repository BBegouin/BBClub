__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.player import Player
from league_manager.views.serializers.roster_list_serializers import RosterLineSerializer
from league_manager.views.serializers.player_evolution_serializer import EvolutionSerializer

class PlayerSerializer(serializers.ModelSerializer):
    ref_roster_line = RosterLineSerializer(many=False,read_only=True)
    evolution = EvolutionSerializer(many=True,read_only=True)
    class Meta:
        model = Player

class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields=('name','ref_roster_line','miss_next_game','num')

class UpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields=('name','miss_next_game','num')
