__author__ = 'Bertrand'

from rest_framework import serializers

class RankingLineSerializer(serializers.Serializer):
    #rank = serializers.IntegerField()
    #trend = serializers.IntegerField()
    team_id = serializers.IntegerField()
    team_name = serializers.CharField()
    ranking_point = serializers.IntegerField()
    played = serializers.IntegerField()
    won = serializers.IntegerField()
    drew = serializers.IntegerField()
    lost = serializers.IntegerField()
    bonus = serializers.IntegerField()
    coach = serializers.CharField()
    td_for = serializers.IntegerField()
    td_against = serializers.IntegerField()
    cas_for = serializers.IntegerField()
    cas_against = serializers.IntegerField()
    aggro = serializers.IntegerField()
    passes = serializers.IntegerField()
    dungeon = serializers.BooleanField()

