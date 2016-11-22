__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.models.team import Team
from league_manager.views.serializers.player_report_serializer import PlayerReportSerializer,CreatePlayerReportSerializer
from rest_framework.exceptions import NotAcceptable

"""
    Sérializer de liste
"""
class TeamReportSerializer(serializers.ModelSerializer):
    player_report = PlayerReportSerializer(many=True)
    class Meta:
        model = TeamReport
        fields=('id','match','team','supporters','fame','winnings','fan_factor','player_report','result')

"""
    Serializer de création conjointe à un rapport de match
"""
class CreateTeamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamReport
        fields=('id','team')


"""
    Serializer de création standalone
"""
class CreateStandaloneTeamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamReport
        fields=('id','team','match')

    def create(self, validated_data):

        # on vérifie que les status de l'équipe est compatible d'une création
        if validated_data.get('team').status != 1 :
                raise NotAcceptable("le statut de l'équipe n'est pas compatible")

        tr = TeamReport.objects.create(**validated_data)
        return tr

"""
Serializer de mise à jour des team reports
"""
class UpdateTeamReportSerializer(serializers.ModelSerializer):
    player_report = CreatePlayerReportSerializer(many=True,allow_null=True)
    supporters = serializers.IntegerField(allow_null=True)
    fame = serializers.IntegerField(allow_null=True)
    winnings = serializers.IntegerField(allow_null=True)
    fan_factor = serializers.IntegerField(allow_null=True)

    class Meta:
        model = TeamReport
        fields=('id','match','team','supporters','fame','winnings','fan_factor','player_report','result')

    def update(self, instance, validated_data):

        # on met à jour les données du rapport d'équipe
        if 'supporters'in validated_data and validated_data.get('supporters', instance.supporters) is not None:
            instance.supporters = validated_data.get('supporters', instance.supporters)

        if 'fame'in validated_data and validated_data.get('fame', instance.fame) is not None:
            instance.fame = validated_data.get('fame', instance.fame)

        if 'winnings'in validated_data:
            winnings = validated_data.get('winnings', instance.winnings)
            if winnings is not None:
                if (winnings <0 or winnings>120):
                    raise NotAcceptable("les gains sont incohérents")
                instance.winnings = winnings

        if 'fan_factor'in validated_data and validated_data.get('fan_factor', instance.fan_factor) is not None:
            instance.fan_factor = validated_data.get('fan_factor', instance.fan_factor)

        if 'other_casualties'in validated_data and validated_data.get('other_casualties', instance.other_casualties) is not None:
            instance.other_casualties = validated_data.get('other_casualties', instance.other_casualties)

        instance.save()

        # En plus de la création, il faut mettre à jour les rapports d'équipe le cas échéant
        if 'player_report' in validated_data:
            player_reports = validated_data.pop('player_report')
            # si on a des players reports, passés en paramètres, il faut les mettre à jour
            if player_reports is not None:
                for player_report in player_reports:
                    PlayerReport.objects.update_or_create(**player_report)

        return instance
