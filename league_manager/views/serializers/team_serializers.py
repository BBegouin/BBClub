__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.team import Team
from league_manager.models.player import Player
from league_manager.views.serializers.roster_list_serializers import RosterListSerializer,RosterLineSerializer
from bbc_user.views.serializers.user_serializer import UserSerializer
from league_manager.views.serializers.player_serializer import PlayerSerializer,CreatePlayerSerializer

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True,read_only=True);
    ref_roster = RosterListSerializer(many=False,read_only=True);
    coach = UserSerializer(many=False,read_only=True);

    class Meta:
        model = Team

class CreateTeamSerializer(serializers.ModelSerializer):
    players = CreatePlayerSerializer(many=True);

    class Meta:
        model = Team
        fields=('name','players','ref_roster','treasury','nb_rerolls','pop','assistants','cheerleaders','apo','coach','icon_file_path','league','DungeonBowl','id')

    def create(self, validated_data):
        players_data = validated_data.pop('players')
        new_team = Team.objects.create(**validated_data)
        for player_data in players_data:
            Player.objects.create(name="",team=new_team, **player_data)
        return new_team