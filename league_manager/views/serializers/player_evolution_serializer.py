__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.player_evolution import PlayerEvolution

class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerEvolution
