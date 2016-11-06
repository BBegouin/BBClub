__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from league_manager.models.team import Team,Player
from league_manager.models.match_report import MatchReport
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.models.ref_roster_line import Ref_Roster_Line
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.team_factories import TeamFactory
from league_manager.tests.factories.match_report_factories import MatchReportFactory
from league_manager.tests.factories.match_report_factories import TeamReportFacory,PlayerReportFactory
from league_manager.tests.datas.input.match_report import *
from league_manager.tests.datas.output.match_report import *
from league_manager.tests.factories.player_factories import PlayerFactory
from django.contrib.auth.models import User
import pytest

mr_root="/match_report/"
mr_publish_root="/match_report/%i/publish/"

"""
On teste :
- la création d'un rapport de match
- la création des rapports d'équipes liés
"""
class TestMatchReport(APITestCase):

    @classmethod
    def setUpTestData(cls):
        #on crée les rapport de match test :
        # Deux rapports de match, opposant :
        #   - la team 1 à la team 2
        #   - la team 1 à la team 4
        # les team sont crées avec tous leurs joueurs

        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        myadmin = AdminFactory.create()

        mr = MatchReportFactory.create()
        mr2 = MatchReportFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)

        pl1 = PlayerFactory.create(team=team1)
        pl2 = PlayerFactory.create(team=team1)
        pl3 = PlayerFactory.create(team=team1)
        pl4 = PlayerFactory.create(team=team1,
                                   ref_roster_line=Ref_Roster_Line.objects.get(pk=16))
        pl5 = PlayerFactory.create(team=team1)
        pl6 = PlayerFactory.create(team=team1)
        pl7 = PlayerFactory.create(team=team1)
        pl8 = PlayerFactory.create(team=team1)
        pl9 = PlayerFactory.create(team=team1)
        pl10 = PlayerFactory.create(team=team1)
        pl11 = PlayerFactory.create(team=team1)

        team2 = TeamFactory.create(user=user2,status=1)

        pl12 = PlayerFactory.create(team=team2)
        pl13 = PlayerFactory.create(team=team2)
        pl14 = PlayerFactory.create(team=team2)
        pl15 = PlayerFactory.create(team=team2)
        pl16 = PlayerFactory.create(team=team2)
        pl17 = PlayerFactory.create(team=team2)
        pl18 = PlayerFactory.create(team=team2)
        pl19 = PlayerFactory.create(team=team2)
        pl20 = PlayerFactory.create(team=team2)
        pl21 = PlayerFactory.create(team=team2)
        pl22 = PlayerFactory.create(team=team2)

        team3 = TeamFactory.create(user=user2,status=3)
        team4 = TeamFactory.create(user=user2,status=1)

        pl23 = PlayerFactory.create(team=team4)
        pl24 = PlayerFactory.create(team=team4)
        pl25 = PlayerFactory.create(team=team4)
        pl26 = PlayerFactory.create(team=team4)
        pl27 = PlayerFactory.create(team=team4)
        pl28 = PlayerFactory.create(team=team4)
        pl29 = PlayerFactory.create(team=team4)
        pl30 = PlayerFactory.create(team=team4)
        pl31 = PlayerFactory.create(team=team4)
        pl32 = PlayerFactory.create(team=team4)
        pl33 = PlayerFactory.create(team=team4)

        team5 = TeamFactory.create(user=user2,status=0)


        tr = TeamReportFacory.create(match=mr,team=team1)

        pr = PlayerReportFactory.create(team_report=tr,player=pl1)
        pr2 = PlayerReportFactory.create(team_report=tr,player=pl2)
        pr3 = PlayerReportFactory.create(team_report=tr,player=pl3)
        pr4 = PlayerReportFactory.create(team_report=tr,player=pl4)

        tr2 = TeamReportFacory.create(match=mr,team=team2)

        pr = PlayerReportFactory.create(team_report=tr2,player=pl12)
        pr2 = PlayerReportFactory.create(team_report=tr2,player=pl13)
        pr3 = PlayerReportFactory.create(team_report=tr2,player=pl14)
        pr4 = PlayerReportFactory.create(team_report=tr2,player=pl15)

        tr3 = TeamReportFacory.create(match=mr2,team=team1,fan_factor=-1,winnings=20)

        PlayerReportFactory.create(team_report=tr3,
                                   player=pl3,
                                   injury_type = 0,
                                   mvp = True)
        PlayerReportFactory.create(team_report=tr3,
                                   player=pl4,
                                   injury_type = 2)
        PlayerReportFactory.create(team_report=tr3,player=pl5,injury_type = 7)

        tr4 = TeamReportFacory.create(match=mr2,team=team4,fan_factor=1,winnings=60)

        PlayerReportFactory.create(team_report=tr4,player=pl23)
        PlayerReportFactory.create(team_report=tr4,player=pl24)
        PlayerReportFactory.create(team_report=tr4,player=pl25)
        PlayerReportFactory.create(team_report=tr4,player=pl26)

    """
        Test de récupération de la liste des rapports de match
    """
    def test_get_match_report_list_success(self):
        mr_count = MatchReport.objects.all().count()
        response = self.client.get(mr_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(list_datas,response.data)

    """
        Test de récupération d'un rapport de match
    """
    def test_get_match_report_detail_success(self):
        # on test la récupération simple
        mr_id = MatchReport.objects.all().first().id
        response = self.client.get(mr_root+"%i/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.assertEqual(response.data, detail_datas)

    """
        Test de récupération de la liste des rapports de match, pour une équipe
    """
    def test_get_match_report_for_team_success(self):

        # si on fait une requête avec le param team, on doit avoir tous les rapport de match pour la team en question
        team_id = Team.objects.filter(status=1).first().id
        response = self.client.get(mr_root+"?team=%i"%team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on compte le nombre d'équipe en BDD
        match_report_cpt = MatchReport.objects.filter(team_reports__team__id=team_id).count()
        # on vérifie que le nombre d'équipe récupéré correspond a celui en BDD
        self.assertEqual(len(response.data),match_report_cpt)

        #on ne vérifie pas le contenu, vérifié par le test de récupération du détail

    """
        Test de création d'un rapport : création anonyme interdite
    """
    def test_create_raport_anonymous_forbidden(self):
        response = self.client.post(mr_root,data=create_datas_step_1_OK)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
        Test de création d'un rapport : nombre de team incompatible anonyme interdite
    """
    def test_create_report_incompatible_team_number_forbidden(self):

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_3)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
        Test de création d'un rapport : état de l'une des équipes incompatible : interdit
    """
    def test_create_report_incompatible_team_forbidden(self):

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on teste avec une équipe dans l'état 3
        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_1)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on teste avec une équipe dans l'état 0
        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_2)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


    """
        Test de la création d'un rapport en phase 1 : succès
    """
    def test_create_match_report_step_1_success(self):
        #on sauvegarde le nombre d'article avant la création
        mr_num = MatchReport.objects.count()
        tr_num = TeamReport.objects.count()

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'un rapport
        response = self.client.post(mr_root,data=create_datas_step_1_OK)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # on vérifie que le rapport est bien créé avec le bon statut
        mr_id = response.data["id"]
        created_mr = MatchReport.objects.get(pk=mr_id)
        self.assertEqual(created_mr.status,0)

        # on vérifie que le nombre de rapport de match a augmenté
        self.assertEqual(MatchReport.objects.all().count(),mr_num+1)

        # on vérifie qu'on a bien deux objets rapport d'équipe qui correspondent au match créé
        tr_cpt = TeamReport.objects.filter(match=mr_id).count()
        self.assertEqual(tr_cpt,2)

        # on vérifie le contenu de la réponse
        self.assertEqual(response.data,response_data_create_step_1)

    """
        Test de la modification d'un rapport
    """
    def test_update_match_report_step_2_success(self):

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'un rapport
        response = self.client.post(mr_root,data=create_datas_step_1_OK)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        mr_id = response.data["id"]
        tr_cpt = TeamReport.objects.filter(match=mr_id).count()
        self.assertEqual(tr_cpt,2)

        # on lance la modification d'un rapport avec les données de la phase 2 du rapport
        response = self.client.patch(mr_root+"%i/"%mr_id,data=update_datas_step_2_OK)
        for k,v in response.data.items():
            self.assertEqual(v,response_data_step_2[k])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,response_data_step_2)

        # on vérifie que nous n'avons toujours que deux rapports pour le match en question
        tr_cpt = TeamReport.objects.filter(match=mr_id).count()
        self.assertEqual(tr_cpt,2)

    """
        Test de suppression : suppression en masse interdite, même pour un admin
    """
    def test_delete_all_team_forbidden(self):
        # on vérifie qu'on ne peut pas faire de suppression en masse
        response = self.client.delete(mr_root)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


        self.client.force_authenticate(user=User.objects.get(username="admin"))
        # on vérifie qu'on ne peut pas faire de suppression en masse, même loggué en admin
        response = self.client.delete(mr_root)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    """
        Test de suppression : seul un admin peut supprimer un rapport de match
    """
    def test_delete_match_report_success(self):

        mr_num = MatchReport.objects.all().count()
        mr_id = MatchReport.objects.first().id
        trs = TeamReport.objects.filter(match=mr_id)
        prs = PlayerReport.objects.filter(team_report__match=mr_id)

        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.delete(mr_root+"%d/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie qu'un admin peut supprimer un rapport de match
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        response = self.client.delete(mr_root+"%d/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # on vérifie la suppression du rapport : on vérifie que le comptage des rapport a diminiué
        mr_num_after_delete = MatchReport.objects.all().count()
        self.assertEqual(mr_num_after_delete,mr_num-1)

        # On vérifie qu'on arrive pas à attraper le match supprimé
        response = self.client.get(mr_root+"%d/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        # On vérifie la suppression en cascade :
        # On vérifie que les rapport d'équipe ont été supprimés
        tr_cpt = trs.count()
        self.assertEqual(tr_cpt,0)

        # On vérifie que les rapports de joueurs ont été supprimés
        pr_count = prs.count()
        self.assertEqual(pr_count,0)

    """
        Test de suppression : la suppression anonyme est interdite
    """
    def test_delete_team_anonymous_forbidden(self):
        # On sauvegarde le nombre de post avant la suppression
        mr_id = MatchReport.objects.first().id

        # on vérifie qu'un utilisateur non identifé n'a pas le droit de faire une suppression
        response = self.client.delete(mr_root+"%d/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
     test de finalisation d'un rapport de match :
        - on détermine les statut gagnant / nul / perdants de chaque rapport d'équipe
        - on calcule les xp de chaque rapport de joueur
        - on détermine les joueurs qui doivent passer au niveau supérieur
    """
    def test_publish_match_report(self):
        # attention cette ligne est surpuissante....
        mr_id = MatchReport.objects.get(pk=2).id

        self.client.force_authenticate(user=User.objects.get(username="admin"))

        response = self.client.patch(mr_publish_root%mr_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que le statut des rapport d'équipes ont été mis à jour
        self.assertEqual(response.data,published_data)

        # on vérifie que les données des équipes ont été mises à jour
        response = self.client.get("/team/1/")
        self.assertEqual(response.data,team_1_after_match)
        response = self.client.get("/team/4/")
        self.assertEqual(response.data,team_4_after_match)
