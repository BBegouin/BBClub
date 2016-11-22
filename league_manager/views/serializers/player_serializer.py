__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.player import Player
from league_manager.views.serializers.roster_list_serializers import RosterLineSerializer
from league_manager.views.serializers.skill_serializer import SkillSerializer
from league_manager.views.serializers.player_upgrade_serializer import UpgradeSerializer

class PlayerForTeamSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    class Meta:
        model = Player
        fields=('id',
                'name',
                'num',
                'ref_roster_line',
                'M',
                'F',
                'Ag',
                'Ar',
                'num',
                'miss_next_game',
                'need_upgrade',
                'total_xp',
                'is_journeyman',
                'skills')

class CreatePlayerSerializer(serializers.ModelSerializer):
    miss_next_game = serializers.BooleanField(default=False)
    need_upgrade = serializers.BooleanField(default=False)
    total_xp = serializers.IntegerField(default=0)

    class Meta:
        model = Player
        fields=('name',
                'ref_roster_line',
                'num',
                'miss_next_game',
                'need_upgrade',
                'total_xp')

class UpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields=('name',
                'miss_next_game',
                'num',
                'total_xp')

class PlayerSerializer(serializers.ModelSerializer):
    ref_roster_line = RosterLineSerializer(many=False,read_only=True)
    evolution = UpgradeSerializer(many=True,read_only=True)
    class Meta:
        model = Player

class PlayerDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    nb_passes = serializers.IntegerField()
    nb_TD = serializers.IntegerField()
    nb_int = serializers.IntegerField()
    nb_cas = serializers.IntegerField()
    nb_MVP = serializers.IntegerField()
    base_cost = serializers.IntegerField()
    evolution_cost = serializers.IntegerField()

    class Meta:
        model = Player
        fields=('id',
                'name',
                'num',
                'ref_roster_line',
                'M',
                'F',
                'Ag',
                'Ar',
                'num',
                'miss_next_game',
                'need_upgrade',
                'nb_passes',
                'nb_TD',
                'nb_int',
                'nb_cas',
                'nb_MVP',
                'total_xp',
                'is_journeyman',
                'skills',
                'base_cost',
                'evolution_cost'
                )
        read_only_fields = (
            'id',
            'name',
            'num',
            'ref_roster_line',
            'M',
            'F',
            'Ag',
            'Ar',
            'num',
            'miss_next_game',
            'need_upgrade',
            'nb_passes',
            'nb_TD',
            'nb_int',
            'nb_cas',
            'nb_MVP',
            'total_xp',
            'is_journeyman',
            'skills'
        )
