__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.player_evolution import PlayerEvolution
from league_manager.views.serializers.skill_serializer import DetailedSkillSerializer

class EvolutionSerializer(serializers.ModelSerializer):
    skill = DetailedSkillSerializer(many=False,read_only=True)
    class Meta:
        model = PlayerEvolution
        fields=("id","skill","value","type","status")

class CreateEvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerEvolution