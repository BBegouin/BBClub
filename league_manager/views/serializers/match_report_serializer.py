__author__ = 'Bertrand'

from rest_framework import serializers
from league_manager.models.match_report import MatchReport
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.views.serializers.team_report_serializer import TeamReportSerializer, CreateTeamReportSerializer,UpdateTeamReportSerializer
from rest_framework.exceptions import NotAcceptable

"""
Match reports
"""
class MatchReportSerializer(serializers.ModelSerializer):
    team_reports = TeamReportSerializer(many=True)

    class Meta:
        model = MatchReport

class CreateMatchReportSerializer(serializers.ModelSerializer):
    team_reports = CreateTeamReportSerializer(many=True)

    class Meta:
        model = MatchReport
        fields=('id','team_reports','status')

    def create(self, validated_data):
        team_reports = validated_data.pop('team_reports')

        if len(team_reports) != 2:
            raise NotAcceptable("un rapport de match ne concerne que deux équipes")

        # on vérifie que les status des équipes sont compatible d'une création
        tr1 = team_reports[0]
        tr2 =  team_reports[1]
        if tr1['team'].status != 1 or \
           tr2['team'].status != 1 :
                raise NotAcceptable("le statut d'une des deux équipes n'est pas compatible")

        mr = MatchReport.objects.create(**validated_data)
        otr1 = TeamReport.objects.create(match=mr,**tr1)
        otr2 = TeamReport.objects.create(match=mr,**tr2)

        return mr


class UpdateMatchReportSerializer(serializers.ModelSerializer):
    team_reports = UpdateTeamReportSerializer(many=True)
    status = serializers.IntegerField(allow_null=True)
    weather = serializers.IntegerField(allow_null=True)
    date = serializers.DateField(allow_null=True)

    class Meta:
        model = MatchReport
        fields=('id','team_reports','status','weather','date')

    """
     La récéption d'un rapport de match doit déclencher la mise à jour, sauf si le rapport de match est déjà publié
    """
    def update(self, instance, validated_data):
        team_reports = validated_data.pop('team_reports')

        if instance.status == 1:
            raise NotAcceptable("impossible de modifier un rapport de match publié")

        # on vérifie que le rapport concerne bien deux équipe
        if len(team_reports) > 2:
            raise NotAcceptable("un rapport de match ne concerne que deux équipes maximum")

        # on vérifie que les status des équipes sont compatible d'une création
        for tr in team_reports:
            if tr['team'].status != 1 :
                raise NotAcceptable("le statut d'une des deux équipes n'est pas compatible")

        # on met à jour les données du rapport de match
        if validated_data.get('weather', instance.weather) is not None:
            instance.weather = validated_data.get('weather', instance.weather)

        if validated_data.get('date', instance.date) is not None:
            instance.date = validated_data.get('date', instance.date)

        instance.save()

        # on met à jour les données des rapports d'équipes
        instance_report_1 = instance.team_reports.all()[0]
        instance_report_2 = instance.team_reports.all()[1]
        if instance_report_1.team == team_reports[0]['team']:
            self.UpdateTeamReport(instance_report_1,team_reports[0])
            if 'player_report' in team_reports[0]:
                self.UpdatePlayerReports(instance_report_1,team_reports[0]['player_report'])

        elif instance_report_1.team == team_reports[1]['team']:
            self.UpdateTeamReport(instance_report_1,team_reports[1])
            if 'player_report' in team_reports[1]:
                self.UpdatePlayerReports(instance_report_1,team_reports[1]['player_report'])

        if instance_report_2.team == team_reports[0]['team']:
            self.UpdateTeamReport(instance_report_2,team_reports[0])
            if 'player_report' in team_reports[0]:
                self.UpdatePlayerReports(instance_report_2,team_reports[0]['player_report'])

        elif instance_report_2.team == team_reports[1]['team']:
            self.UpdateTeamReport(instance_report_2,team_reports[1])
            if 'player_report' in team_reports[1]:
                self.UpdatePlayerReports(instance_report_2,team_reports[1]['player_report'])

        return instance

    def UpdateTeamReport(self,target,source):
        try:
            target.supporters = source['supporters']
        except BaseException :
            pass

        try:
            target.fame = source['fame']
        except BaseException :
            pass

        try:
            target.winnings = source['winnings']
        except BaseException :
            pass

        try:
            target.fan_factor = source['fan_factor']
        except BaseException :
            pass

        try:
            target.other_casualties = source['other_casualties']
        except BaseException :
            pass

        target.save()

    """
     on crée les rapport, si la cible ne contient pas déjà des rapports d'équipe
    """
    def UpdatePlayerReports(self,target,source):
        for player_report in source:
            PlayerReport.objects.update_or_create(**player_report)




