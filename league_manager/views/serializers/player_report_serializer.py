__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.player_report import PlayerReport


"""
player reports
"""
class PlayerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerReport

class CreatePlayerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerReport
