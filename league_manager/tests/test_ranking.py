__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase

from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.match_report_factories import MatchReportFactory,TeamReportFacory,PlayerReportFactory
from league_manager.tests.factories.player_factories import PlayerFactory
from league_manager.tests.factories.team_factories import TeamFactory

from league_manager.tests.datas.output import *
from django.contrib.auth.models import User

ranking_root="/ranking/"

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestTeam(APITestCase):

    created_team_id = 0

    #on crée 6 équipes A,B,C,D,E,F de 5 joueurs chacune A1...A5
    #on crée 7 matchs
    # A vs B : TD 1-0 ; SOR 2-0 ; AGRO 1-0 ; REU 1-0
    # C vs D : TD 3-0 ; SOR 0-1 ; AGRO 3-0 ; REU 0-1
    # E vs F : TD 1-1 ; SOR 2-3 ; AGRO 1-0 ; REU 0-1
    # B vs C : TD 0-1 ; SOR 5-0 ; AGRO 1-0 ; REU 1-0
    # D vs E : TD 0-1 ; SOR 0-1 ; AGRO 1-0 ; REU 1-0
    # F vs A : TD 1-1 ; SOR 1-0 ; AGRO 1-0 ; REU 0-1

    # ce qui doit nous donner le classement suivant
    # A : 1v 1n 0d : 6pts : 4pts bonus
    # B : 0v 0n 2d : 2pts : 5pts bonus
    # C : 2v 0n 0d : 8pts : 2pts bonus
    # D : 0v 0n 2d : 2pts : 1pts bonus
    # E : 1v 1n 0d : 6pts : 5pts bonus
    # F : 0v 2n 0d : 4pts : 6pts bonus

    #                         J G N P   TD+ TD-  SOR+ SOR-   reu   agro
    # C : 8pts : 4pts bonus : 2 2 0 0 :  4   0 : 0   6     :  0  :  3
    # E : 6pts : 5pts bonus : 2 1 1 0 :  2   1 : 3   3     :  0  :  1
    # A : 6pts : 4pts bonus : 2 1 1 0 :  2   1 : 2   1     :  2  :  1
    # F : 4pts : 6pts bonus : 2 0 2 0 :  2   2 : 4   2     :  1  :  1
    # B : 2pts : 5pts bonus : 2 0 0 2 :  0   2 : 5   2     :  1  :  1
    # D : 2pts : 1pts bonus : 2 0 0 2 :  0   4 : 1   1     :  2  :  1

    def createData(self):
        myuser = UserFactory.create()
        userB = UserFactory.create(username="userB",password="userB")
        userC = UserFactory.create(username="userC",password="userC")
        userD = UserFactory.create(username="userD",password="userD")
        userE = UserFactory.create(username="userE",password="userE")
        userF = UserFactory.create(username="userF",password="userF")

        teamA = TeamFactory.create(user=myuser,status=1,name="teamA")
        plA1 = PlayerFactory.create(team=teamA)
        plA2 = PlayerFactory.create(team=teamA)
        plA3 = PlayerFactory.create(team=teamA)
        plA4 = PlayerFactory.create(team=teamA)
        plA5 = PlayerFactory.create(team=teamA)

        teamB = TeamFactory.create(user=userB,status=1,name="teamB")
        plB1 = PlayerFactory.create(team=teamB)
        plB2 = PlayerFactory.create(team=teamB)
        plB3 = PlayerFactory.create(team=teamB)
        plB4 = PlayerFactory.create(team=teamB)
        plB5 = PlayerFactory.create(team=teamB)

        teamC = TeamFactory.create(user=userC,status=1,name="teamC")
        plC1 = PlayerFactory.create(team=teamC)
        plC2 = PlayerFactory.create(team=teamC)
        plC3 = PlayerFactory.create(team=teamC)
        plC4 = PlayerFactory.create(team=teamC)
        plC5 = PlayerFactory.create(team=teamC)

        teamD = TeamFactory.create(user=userD,status=1,name="teamD")
        plD1 = PlayerFactory.create(team=teamD)
        plD2 = PlayerFactory.create(team=teamD)
        plD3 = PlayerFactory.create(team=teamD)
        plD4 = PlayerFactory.create(team=teamD)
        plD5 = PlayerFactory.create(team=teamD)

        teamE = TeamFactory.create(user=userE,status=1,name="teamE")
        plE1 = PlayerFactory.create(team=teamE)
        plE2 = PlayerFactory.create(team=teamE)
        plE3 = PlayerFactory.create(team=teamE)
        plE4 = PlayerFactory.create(team=teamE)
        plE5 = PlayerFactory.create(team=teamE)

        teamF = TeamFactory.create(user=userF,status=1,name="teamF")
        plF1 = PlayerFactory.create(team=teamF)
        plF2 = PlayerFactory.create(team=teamF)
        plF3 = PlayerFactory.create(team=teamF)
        plF4 = PlayerFactory.create(team=teamF)
        plF5 = PlayerFactory.create(team=teamF)

        # -------------  Match A - B
        # A vs B : TD 1-0 ; SOR 2-0 ; AGRO 1-0 ; REU 1-0
        mrAB = MatchReportFactory.create(status=0)
        mrAB_trA = TeamReportFacory.create(match=mrAB,team=teamA)

        prA1 = PlayerReportFactory.create(team_report=mrAB_trA,
                                        player=plA1,
                                        nb_td=1,
                                        nb_pass=1)
        prA2 = PlayerReportFactory.create(team_report=mrAB_trA,
                                        player=plA2,
                                        nb_cas=1,
                                        nb_foul=1)
        prA3 = PlayerReportFactory.create(team_report=mrAB_trA,
                                        player=plA3,
                                        nb_cas=1)

        mrAB_trB = TeamReportFacory.create(match=mrAB,team=teamB)

        mrAB.publish()

        # -------------  Match C - D
        # C vs D : TD 3-0 ; SOR 0-1 ; AGRO 3-0 ; REU 0-1
        mrCD = MatchReportFactory.create(status=0)
        mrCD_trC = TeamReportFacory.create(match=mrCD,team=teamC)

        prCD_trC_C1 = PlayerReportFactory.create(team_report=mrCD_trC,
                                        player=plC1,
                                        nb_td=2,
                                        nb_pass=0)
        prCD_trC_C2 = PlayerReportFactory.create(team_report=mrCD_trC,
                                        player=plC2,
                                        nb_td=1,
                                        nb_cas=0,
                                        nb_foul=1)
        prCD_trC_C3 = PlayerReportFactory.create(team_report=mrCD_trC,
                                        player=plC3,
                                        nb_td=0,
                                        nb_cas=0,
                                        nb_foul=2)

        mrCD_trD = TeamReportFacory.create(match=mrCD,team=teamD)

        prCD_trC_D1 = PlayerReportFactory.create(team_report=mrCD_trD,
                                        player=plD1,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_pass=0)
        prCD_trC_D2 = PlayerReportFactory.create(team_report=mrCD_trD,
                                        player=plD2,
                                        nb_td=0,
                                        nb_pass=1)

        mrCD.publish()

        # -------------  Match E - F
        # E vs F : TD 1-1 ; SOR 2-3 ; AGRO 1-0 ; REU 0-1
        mrEF = MatchReportFactory.create(status=0)
        mrEF_trE = TeamReportFacory.create(match=mrEF,team=teamE)

        mrEF_trE_E1 = PlayerReportFactory.create(team_report=mrEF_trE,
                                        player=plE1,
                                        nb_td=1,
                                        nb_pass=0)
        mrEF_trE_E2 = PlayerReportFactory.create(team_report=mrEF_trE,
                                        player=plE2,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=1)
        mrEF_trE_E3 = PlayerReportFactory.create(team_report=mrEF_trE,
                                        player=plE3,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=0)

        mrEF_trF = TeamReportFacory.create(match=mrEF,team=teamF)
        mrEF_trF_F1 = PlayerReportFactory.create(team_report=mrEF_trF,
                                        player=plF1,
                                        nb_td=1,
                                        nb_pass=1)
        mrEF_trF_F2 = PlayerReportFactory.create(team_report=mrEF_trF,
                                        player=plF2,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=0)
        mrEF_trF_F3 = PlayerReportFactory.create(team_report=mrEF_trF,
                                        player=plF3,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=0)
        mrEF_trF_F4 = PlayerReportFactory.create(team_report=mrEF_trF,
                                        player=plF4,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=0)

        mrEF.publish()

        # -------------  Match B - C
        # B vs C : TD 0-1 ; SOR 5-0 ; AGRO 1-0 ; REU 1-0
        mrBC = MatchReportFactory.create(status=0)
        mrBC_trB = TeamReportFacory.create(match=mrBC,team=teamB)

        mrBC_trB_B1 = PlayerReportFactory.create(team_report=mrBC_trB,
                                        player=plB5,
                                        nb_td=0,
                                        nb_cas=2,
                                        nb_pass=1)
        mrEF_trE_B2 = PlayerReportFactory.create(team_report=mrBC_trB,
                                        player=plB4,
                                        nb_td=0,
                                        nb_cas=2,
                                        nb_foul=1)
        mrEF_trE_B3 = PlayerReportFactory.create(team_report=mrBC_trB,
                                        player=plB3,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=0)

        mrBC_trC = TeamReportFacory.create(match=mrBC,team=teamC)

        mrBC_trC_C5 = PlayerReportFactory.create(team_report=mrBC_trC,
                                        player=plC5,
                                        nb_td=1,
                                        nb_cas=0,
                                        nb_pass=0)

        mrBC.publish()

        # -------------  Match D - E
        # D vs E : TD 0-1 ; SOR 0-1 ; AGRO 1-0 ; REU 1-0
        mrDE = MatchReportFactory.create(status=0)
        mrDE_trD = TeamReportFacory.create(match=mrDE,team=teamD)

        mrDE_trD_D5 = PlayerReportFactory.create(team_report=mrDE_trD,
                                        player=plD5,
                                        nb_td=0,
                                        nb_cas=0,
                                        nb_pass=1)
        mrDE_trD_D4 = PlayerReportFactory.create(team_report=mrDE_trD,
                                        player=plD4,
                                        nb_td=0,
                                        nb_cas=0,
                                        nb_foul=1)

        mrDE_trE = TeamReportFacory.create(match=mrDE,team=teamE)

        mrDE_trE_E5 = PlayerReportFactory.create(team_report=mrDE_trE,
                                        player=plE5,
                                        nb_td=1,
                                        nb_cas=0,
                                        nb_pass=0)

        mrDE_trE_E4 = PlayerReportFactory.create(team_report=mrDE_trE,
                                        player=plE4,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_pass=0)
        mrDE.publish()

        # -------------- Match F - A
        # F vs A : TD 1-1 ; SOR 1-0 ; AGRO 1-0 ; REU 0-1
        mrFA = MatchReportFactory.create(status=0)
        mrFA_trF = TeamReportFacory.create(match=mrFA,team=teamF)

        mrFA_trF_F5 = PlayerReportFactory.create(team_report=mrFA_trF,
                                        player=plF5,
                                        nb_td=1,
                                        nb_cas=0,
                                        nb_pass=0)
        mrFA_trF_F4 = PlayerReportFactory.create(team_report=mrFA_trF,
                                        player=plF4,
                                        nb_td=0,
                                        nb_cas=1,
                                        nb_foul=1)

        mrFA_trA = TeamReportFacory.create(match=mrFA,team=teamA)

        mrFA_trA_A5 = PlayerReportFactory.create(team_report=mrFA_trA,
                                        player=plA5,
                                        nb_td=1,
                                        nb_cas=0,
                                        nb_pass=1)
        mrFA.publish()

    """
     Test de récupération d'un classement
    """
    def test_get_ranking_success(self):

        self.createData()
        #création des données de base

        response = self.client.get(ranking_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        ranking_datas = [
        { "team_name":"teamC", "team_id":3, "ranking_point":8, "played":2, "won": 2, "drew":0, "lost":0, "bonus":4, "coach":"userC", "td_for":4,"td_against":0,"cas_for":0,"cas_against":6,"aggro":3,"passes":0,"dungeon":False,},
        { "team_name":"teamE", "team_id":5, "ranking_point":6, "played":2, "won": 1, "drew":1, "lost":0, "bonus":5, "coach":"userE", "td_for":2,"td_against":1,"cas_for":3,"cas_against":3,"aggro":1,"passes":0,"dungeon":False,},
        { "team_name":"teamA", "team_id":1, "ranking_point":6, "played":2, "won": 1, "drew":1, "lost":0, "bonus":4, "coach":"john_doe", "td_for":2,"td_against":1,"cas_for":2,"cas_against":1,"aggro":1,"passes":2,"dungeon":False,},
        { "team_name":"teamF", "team_id":6, "ranking_point":4, "played":2, "won": 0, "drew":2, "lost":0, "bonus":6, "coach":"userF", "td_for":2,"td_against":2,"cas_for":4,"cas_against":2,"aggro":1,"passes":1,"dungeon":False,},
        { "team_name":"teamB", "team_id":2, "ranking_point":2, "played":2, "won": 0, "drew":0, "lost":2, "bonus":5, "coach":"userB", "td_for":0,"td_against":2,"cas_for":5,"cas_against":2,"aggro":1,"passes":1,"dungeon":False,},
        { "team_name":"teamD", "team_id":4, "ranking_point":2, "played":2, "won": 0, "drew":0, "lost":2, "bonus":1, "coach":"userD", "td_for":0,"td_against":4,"cas_for":1,"cas_against":1,"aggro":1,"passes":2,"dungeon":False,},
        ]

        self.assertEqual(response.data,ranking_datas)






