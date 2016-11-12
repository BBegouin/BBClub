__author__ = 'Bertrand'
from league_manager.models.team import Team
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.models.match_report import MatchReport
from django.db.models import Sum

class RankingLine(object):

    """
    Constructeur à partir de la référence d'une équipe
    La paramètre team est une instance de model de Team
    """
    def __init__(self, team):
        all_reports = PlayerReport.objects.filter(team_report__team=team,team_report__match__status=1)

        self.team_name = team.name
        self.team_id = team.pk
        self.ranking_point = team.ranking_points
        self.played = TeamReport.objects.filter(team=team,match__status=1).count()
        self.won = TeamReport.objects.filter(team=team,match__status=1,result=0).count()
        self.drew = TeamReport.objects.filter(team=team,match__status=1,result=1).count()
        self.lost =  TeamReport.objects.filter(team=team,match__status=1,result=2).count()
        self.bonus = team.bonus_point
        self.coach = team.user
        res = all_reports.aggregate(TD=Sum('nb_td'))
        self.td_for = res['TD']
        #il faut sélectionner toutes les équipes qui ont joué contre l'équipe courante, c'est à dire :
        all_reports_against = PlayerReport.objects.filter(team_report__match__team_reports__team=team).exclude(team_report__team=team,)
        #- On sélectionne tous les rapports de joueurs qui appartiennent à un rapport d'équipe qui est liés à un rapport de
        #match qui contient un rapport de match de l'équipe courante, en excluant les rapports de joueurs de l'équipe
        #courante
        res =  all_reports_against.aggregate(TD=Sum('nb_td'))
        self.td_against = res['TD']
        res = all_reports.aggregate(CAS=Sum('nb_cas'))
        self.cas_for = res['CAS']
        res = all_reports_against.aggregate(CAS=Sum('nb_cas'))
        self.cas_against = res['CAS']
        res = all_reports.aggregate(AGRO=Sum('nb_foul'))
        self.aggro = res['AGRO']
        res = all_reports.aggregate(REU=Sum('nb_pass'))
        self.passes = res['REU']
        self.dungeon = team.DungeonBowl

         #Construction de la tendance : il faut voir si l'équipe monte ou si elle baisse





