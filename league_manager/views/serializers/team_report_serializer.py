__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.team_report import TeamReport
from league_manager.views.serializers.player_report_serializer import PlayerReportSerializer,CreatePlayerReportSerializer

"""
team reports
"""
class TeamReportSerializer(serializers.ModelSerializer):
    player_report = PlayerReportSerializer(many=True)
    class Meta:
        model = TeamReport
        fields=('id','match','team','supporters','fame','winnings','fan_factor','player_report')

class CreateTeamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamReport
        fields=('id','team',)

class UpdateTeamReportSerializer(serializers.ModelSerializer):
    player_report = CreatePlayerReportSerializer(many=True,allow_null=True)
    supporters = serializers.IntegerField(allow_null=True)
    fame = serializers.IntegerField(allow_null=True)
    winnings = serializers.IntegerField(allow_null=True)
    fan_factor = serializers.IntegerField(allow_null=True)

    class Meta:
        model = TeamReport
        fields=('id','match','team','supporters','fame','winnings','fan_factor','player_report')