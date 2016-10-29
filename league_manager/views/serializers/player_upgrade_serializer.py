__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.team import Team
from league_manager.models.player import Player
from league_manager.views.serializers.skill_serializer import DetailedSkillSerializer
from rest_framework.exceptions import NotAcceptable

class UpgradeSerializer(serializers.ModelSerializer):
    skill = DetailedSkillSerializer(many=False,read_only=True)
    class Meta:
        model = PlayerUpgrade
        fields=("id","skill","value","type","status")

"""
Serializer de création :
si un upgrade est crée sur un joueur dont la team à pour status :
 - est 0 : la création doit être considéré comme un ajout de base et donc vérifier les règles de création
 - est 1 : la création est refusée
 - est 2 : création considérée comme une montée de niveau,
 il faut vérifier que le joueur est susceptible de monter de niveau
 après la création il faut également vérifier si il reste d'autre upgrade à faire,
 sinon il faut passer le status de l'équipe à 3
 - est 3 : création refusée
"""
class CreateUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerUpgrade

    # si la team est au status 0, alors les upgrades sont considérées comme des ajouts de base
    def create(self, validated_data):
        players_data = validated_data.pop('players')
        new_team = Team.objects.create(**validated_data)
        for player_data in players_data:
            Player.objects.create(team=new_team, **player_data)

        if new_team.check_team_price() is False:
            raise NotAcceptable("L'équipe ne respecte pas le budget")

        return new_team