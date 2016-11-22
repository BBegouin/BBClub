__author__ = 'Bertrand'
from django.db import models
from league_manager.models.player_report import PlayerReport
from league_manager.models.team_report import TeamReport
from league_manager.models.player import Player
from league_manager.models.team import Team
from rest_framework.exceptions import NotAcceptable
from django.db.models import Sum
from django.db.models import F

class MatchReport(models.Model):
    date = models.DateField("Date de la rencontre",null=True)
    # 0: Canicule
    # 1: Très ensoleillé
    # 2: Clément
    # 3: Averse
    # 4: Blizzard
    weather = models.CharField(max_length=50,null=True)
    # status value :
    # 0 : draft : default value
    # 1 : published : impossible to modify
    status = models.PositiveSmallIntegerField(blank=False,null=False)


    """
     Sert à valider un rapport de match.
     Lors de la validation d'un rapport de match :
     1- on met à jour les joueurs de l'équipe
        - Xp
        - upgrade
        - blessures
        - downgrade
     2- on met à jour le rapport d'équipe :
        - statut gagné / nul / perdu
     2- on met à jour l'équipe :
        - pop
        - trésorerie
        -
    """
    def publish(self):
        #on met à jour les rapports d'équipes : on met à jour le statut gagnant / perdant
        self.update_team_reports()

        # on met à jour les données des rapports de joueurs
        self.update_player_reports()

        # on met à jour les données des joueurs
        self.update_players()

        # on met à jour les données des équipes
        self.update_team_datas()

        self.status = 1
        self.save()

    """
     On compare le nombre de TD inscrit par chacune des équipe afin de déterminer le gagnant et le perdant
    """
    def update_team_reports(self):

        team_reports = TeamReport.objects.filter(match=self)
        if team_reports.count() != 2:
            raise NotAcceptable("On doit avoir 2 rapport d'équipes par rapport de match, ni plus ni moins")
        td_team1 = team_reports[0].player_report.aggregate(td_count=Sum('nb_td'))
        td_team2 = team_reports[1].player_report.aggregate(td_count=Sum('nb_td'))
        tr1 = TeamReport.objects.get(pk=team_reports[0].id)
        tr2 = TeamReport.objects.get(pk=team_reports[1].id)

        if td_team1["td_count"] is None :
            td_team1["td_count"] = 0
        if td_team2["td_count"] is None:
            td_team2["td_count"] = 0

        if td_team1["td_count"] == td_team2["td_count"]:
            tr1.result = 1
            tr2.result = 1
        elif td_team1["td_count"] > td_team2["td_count"]:
            tr1.result = 0
            tr2.result = 2
        elif td_team1["td_count"] < td_team2["td_count"]:
            tr1.result = 2
            tr2.result = 0

        tr1.save()
        tr2.save()

    """
     la publication nécessite le calcul des xp gagnés
    """
    def update_player_reports(self):
        prs = PlayerReport.objects.filter(team_report__match=self)
        for pr in prs:
            pr.update_earned_xps()


    """
     la publication d'un rapport permettre de mettre à jour les données des joueurs :
     - les stats
     - les comps
     - les xps
     - le status need-upgrade
     - le status MNG

     On update tous les joueurs, car même ceux qui n'ont pas joué pour cause de blessure,
     ne doivent plus être blessés à l'issue de ce match
    """
    def update_players(self):
        players = Player.objects.filter(team__report__match=self)
        for pr in players:
            pr.update_datas()

    """
     On met à jour les données des équipes impliquées dans le match :
      - évolution de la pop
      - TV : sur la base des xp des joueurs. Un choix de skill ultérieur remettra le TV à jour
      - ranking_points : points de classement basé sur les règles de ligue
      - bonus_point : points bonus basé sur les règles de ligue
    """
    def update_team_datas(self):
        teams = Team.objects.filter(report__match=self)
        # évolution de la pop
        for team in teams:
            tr = TeamReport.objects.get(match=self,team=team)
            team.pop += tr.fan_factor
            team.treasury += tr.winnings
            team.update_ranking_point()
            team.update_bonus_point()
            team.update_Journeymen()
            team.update_TV()
            team.save()






    """
     Sert à dé-valider un rapport de match.
     Lors de la dé-validation d'un rapport de match :
     1- on met à jour les joueurs de l'équipe
        - Xp
        - upgrade
        - blessures
        - downgrade
     2- on met à jour le rapport d'équipe :
        - statut gagné / nul / perdu
     2- on met à jour l'équipe :
        - pop
        - trésorerie
        -
    """
    def unpublish(self):
        pass


