__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from league_manager.models.team import Team,Player
from league_manager.models.match_report import MatchReport
from league_manager.models.team_report import TeamReport
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.team_factories import TeamFactory
from league_manager.tests.factories.match_report_factories import MatchReportFactory
from league_manager.tests.factories.match_report_factories import TeamReportFacory,PlayerReportFactory
from league_manager.tests.datas.input.team_report import *
from league_manager.tests.datas.output.team_report import *
from league_manager.tests.factories.player_factories import PlayerFactory
from django.contrib.auth.models import User
import collections
import json

from deepdiff import DeepDiff
from pprint import pprint


tr_root="/team_report/"

"""
il faut tester :
 -
 -
"""
class TestTeamReport(APITestCase):

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
        team2 = TeamFactory.create(user=user2,status=1)
        team3 = TeamFactory.create(user=user2,status=3)
        team4 = TeamFactory.create(user=user2,status=1)
        team5 = TeamFactory.create(user=user2,status=0)

        pl1 = PlayerFactory.create(team=team1)
        pl2 = PlayerFactory.create(team=team1)
        pl3 = PlayerFactory.create(team=team1)
        pl4 = PlayerFactory.create(team=team1)
        pl5 = PlayerFactory.create(team=team1)
        pl6 = PlayerFactory.create(team=team1)
        pl7 = PlayerFactory.create(team=team1)
        pl8 = PlayerFactory.create(team=team1)
        pl9 = PlayerFactory.create(team=team1)
        pl10 = PlayerFactory.create(team=team1)
        pl11 = PlayerFactory.create(team=team1)

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

        pl23 = PlayerFactory.create(team=team4)
        pl24 = PlayerFactory.create(team=team4)
        pl25 = PlayerFactory.create(team=team4)
        pl45 = PlayerFactory.create(team=team4)
        pl46 = PlayerFactory.create(team=team4)
        pl47 = PlayerFactory.create(team=team4)
        pl48 = PlayerFactory.create(team=team4)
        pl49 = PlayerFactory.create(team=team4)
        pl50 = PlayerFactory.create(team=team4)
        pl51 = PlayerFactory.create(team=team4)
        pl52 = PlayerFactory.create(team=team4)

        tr = TeamReportFacory.create(match=mr,team=team1)
        tr2 = TeamReportFacory.create(match=mr,team=team2)
        tr3 = TeamReportFacory.create(match=mr2,team=team1)

        pr = PlayerReportFactory.create(team_report=tr,player=pl1)
        pr2 = PlayerReportFactory.create(team_report=tr,player=pl2)
        pr3 = PlayerReportFactory.create(team_report=tr,player=pl3)
        pr4 = PlayerReportFactory.create(team_report=tr,player=pl4)

        pr = PlayerReportFactory.create(team_report=tr2,player=pl12)
        pr2 = PlayerReportFactory.create(team_report=tr2,player=pl13)
        pr3 = PlayerReportFactory.create(team_report=tr2,player=pl14)

        PlayerReportFactory.create(team_report=tr3,player=pl3)
        PlayerReportFactory.create(team_report=tr3,player=pl4)
        PlayerReportFactory.create(team_report=tr3,player=pl5)


    """
     Test de récupération de la liste des rapports de d'équipe
    """
    def test_get_team_report_list_success(self):
        tr_count = TeamReport.objects.all().count()
        response = self.client.get(tr_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),tr_count)

        # pour une raison que j'ignore la comparaison directe ne fonctionne pas
        cpt = 0;
        for mr in response.data:
            self.assertEqual(mr,list_datas[cpt])
            cpt +=1

    """
     Test de récupération d'un rapport d'équipe
    """
    def test_get_team_report_detail_success(self):
        # on test la récupération simple
        tr_id = MatchReport.objects.all().first().id
        response = self.client.get(tr_root+"%i/"%tr_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,detail_datas)


    """
        Test de récupération de la liste des rapports de match, pour une équipe
    """
    def test_get_team_report_for_team_success(self):

        # si on fait une requête avec le param team, on doit avoir tous les rapport de match pour la team en question
        team_id = Team.objects.filter(status=1).first().id
        response = self.client.get(tr_root+"?team=%i"%team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on compte le nombre d'équipe en BDD
        match_report_cpt = MatchReport.objects.filter(team_reports__team__id=team_id).count()
        # on vérifie que le nombre d'équipe récupéré correspond a celui en BDD
        self.assertEqual(len(response.data),match_report_cpt)

        #on ne vérifie pas le contenu, vérifié par le test de récupération du détail

    """
        Test de création d'un rapport : création anonyme interdite
    """
    def test_create_report_anonymous_forbidden(self):
        response = self.client.post(tr_root,data=create_datas_OK)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
        Test de création d'un rapport : état de l'équipe incompatible
    """
    def test_create_report_incompatible_team_forbidden(self):

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on teste avec une équipe dans l'état 3
        response = self.client.post(tr_root,data=create_datas_incompatible_team_1)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on teste avec une équipe dans l'état 0
        response = self.client.post(tr_root,data=create_datas_incompatible_team_2)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
        test de la création d'un rapport d'équipe : succès
    """
    def test_create_team_report_step_1_success(self):
        #on sauvegarde le nombre d'article avant la création
        tr_num = TeamReport.objects.count()

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'un rapport
        response = self.client.post(tr_root,data=create_datas_OK)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # on vérifie que le rapport est bien créé avec le bon statut
        tr_id = response.data["id"]

        # on vérifie que le nombre de rapport d'équipe a augmenté
        self.assertEqual(TeamReport.objects.all().count(),tr_num+1)

        # on vérifie le contenu de la réponse de création
        self.assertEqual(response.data,response_create_datas_OK)

    """
        test de la mise à jour d'un rapport d'équipe
    """
    def test_update_match_report_step_2_success(self):

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'un rapport
        response = self.client.post(tr_root,data=create_datas_OK)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        tr_id = response.data["id"]

        # on lance la modification d'un rapport avec les données de la phase 2 du rapport
        response = self.client.patch(tr_root+"%i/"%tr_id,data=update_datas_step_1_OK)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,reponse_update_data_step_1_OK)

        # on lance la modification d'un rapport avec les données de la phase 3 du rapport
        response = self.client.patch(tr_root+"%i/"%tr_id,data=update_datas_step_2_OK)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,reponse_update_datas_step_2_OK)

        # on lance la modification d'un rapport avec les données de la phase 3 du rapport
        response = self.client.patch(tr_root+"%i/"%tr_id,data=update_datas_step_3_OK)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,reponse_update_datas_step_3_OK)

    """
     Test du calcul des xp, test de la création des upgrades de joueurs : TBD
    """

    """
     Test de suppression : suppression en masse interdite
    """
    def test_delete_all_team_forbidden(self):
        # on vérifie qu'on ne peut pas faire de suppression en masse
        response = self.client.delete(tr_root)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="admin"))
        # on vérifie qu'on ne peut pas faire de suppression en masse, même loggué en admin
        response = self.client.delete(tr_root)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)


    """
        Test de suppression d'un rapport : suppression d'un rapport standalone interdite
    """
    def test_delete_team_anonymous_forbidden(self):
        # On sauvegarde le nombre de post avant la suppression
        team_num = Team.objects.count()

        # on vérifie qu'un utilisateur non identifé n'a pas le droit de faire une suppression
        first_team_id = Team.objects.first().id
        response = self.client.delete(tr_root+"%i/"%first_team_id)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # même un utilisateur authentifié ne peut supprimer un rapport lui même
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        user1_team_id = TeamReport.objects.filter(team__user__username="john_doe").first().id
        response = self.client.delete(tr_root+"%d/"%user1_team_id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


