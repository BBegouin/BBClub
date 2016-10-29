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
from league_manager.tests.datas.match_report_datas import *
from league_manager.tests.factories.player_factories import PlayerFactory
from django.contrib.auth.models import User

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


        tr = TeamReportFacory.create(match=mr,team=team1)
        tr2 = TeamReportFacory.create(match=mr,team=team2)
        tr3 = TeamReportFacory.create(match=mr2,team=team1)
        tr4 = TeamReportFacory.create(match=mr2,team=team4)

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

        pr = PlayerReportFactory.create(team_report=tr,player=pl1)
        pr2 = PlayerReportFactory.create(team_report=tr,player=pl2)
        pr3 = PlayerReportFactory.create(team_report=tr,player=pl3)
        pr4 = PlayerReportFactory.create(team_report=tr,player=pl4)

        pr = PlayerReportFactory.create(team_report=tr2,player=pl12)
        pr2 = PlayerReportFactory.create(team_report=tr2,player=pl13)
        pr3 = PlayerReportFactory.create(team_report=tr2,player=pl14)
        pr4 = PlayerReportFactory.create(team_report=tr2,player=pl15)


        PlayerReportFactory.create(team_report=tr3,player=pl3)
        PlayerReportFactory.create(team_report=tr3,player=pl4)
        PlayerReportFactory.create(team_report=tr3,player=pl5)

        PlayerReportFactory.create(team_report=tr4,player=pl23)
        PlayerReportFactory.create(team_report=tr4,player=pl24)
        PlayerReportFactory.create(team_report=tr4,player=pl25)



    """
        Test de récupération de la liste des rapports de match
    """

    def test_get_match_report_list_success(self):
        mr_count = MatchReport.objects.all().count()
        response = self.client.get(mr_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),mr_count)

        cpt = 0;
        for mr in response.data:
            self.assertEqual(mr,list_datas[cpt])
            cpt +=1

    """
     Test de récupération de la liste des rapports de match


    def test_get_match_report_detail_success(self):
        # on test la récupération simple
        mr_id = MatchReport.objects.all().first().id
        response = self.client.get(mr_root+"%i/"%mr_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        for k,v in response.data.items():
            if k == "id":
                continue
            self.assertEqual(v,detail_datas[k])


     Test de récupération de la liste des rapports de match, pour une équipe


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


     Test de création d'un rapport : création anonyme interdite

    def test_create_raport_anonymous_forbidden(self):
        response = self.client.post(mr_root,data=create_datas_step_1_OK)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


     Test de création d'un rapport : nombre de team incompatible anonyme interdite

    def test_create_report_incompatible_team_number_forbidden(self):

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_3)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


     Test de création d'un rapport : état de l'une des équipes incompatible : interdit

    def test_create_report_incompatible_team_forbidden(self):

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on teste avec une équipe dans l'état 3
        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_1)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on teste avec une équipe dans l'état 0
        response = self.client.post(mr_root,data=create_datas_step_1_incompatible_team_2)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


    test de la création d'un rapport en phase 1 : succès

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

    test de la modification d'un rapport pour ajouter la phase 2 : succès

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

        # on vérifie que nous n'avaons toujours que deux rapports pour le match en question
        tr_cpt = TeamReport.objects.filter(match=mr_id).count()
        self.assertEqual(tr_cpt,2)

        # on lance la modification d'un rapport avec les données de la phase 3 du rapport
        response = self.client.patch(mr_root+"%i/"%mr_id,data=update_datas_step_3)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        for k,v in response.data.items():
            self.assertEqual(v,response_data_step_3[k])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,response_data_step_3)



     Test de création d'une équipe : création d'une équipe trop chère interdite

    #il faut également vérifier que seule une team qui contient des joueurs de son roster puisse être crée
    def test_create_team_with_wrong_players_forbidden(self):
        #TBD
        self.assertTrue(True)


     Test de suppression : suppression en masse interdite

    def test_delete_all_team_forbidden(self):
        # on vérifie qu'on ne peut pas faire de suppression en masse
        response = self.client.delete(team_root)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="admin"))
        # on vérifie qu'on ne peut pas faire de suppression en masse, même loggué en admin
        response = self.client.delete(team_root)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)



     Test de suppression d'une équipe : suppression anonyme interdite

    def test_delete_team_anonymous_forbidden(self):
        # On sauvegarde le nombre de post avant la suppression
        team_num = Team.objects.count()

        # on vérifie qu'un utilisateur non identifé n'a pas le droit de faire une suppression
        first_team_id = Team.objects.first().id
        response = self.client.delete(team_root+"%i/"%first_team_id)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    # on vérifie que l'utilisateur connecté a bien le droit de supprimer une de ses propres team
    def test_delete_team_success(self):
        team_num = Team.objects.all().count()
        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        # on vérifie qu'on a le droit de supprimer une de ses propres team
        user1_team_id = Team.objects.filter(user__username="john_doe").first().id
        response = self.client.delete(team_root+"%d/"%user1_team_id)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # on vérifie la suppression du post : on vérifie que le comptage des team a diminiué
        team_num_after_delete = Team.objects.all().count()
        self.assertEqual(team_num_after_delete,team_num-1)

        # On vérifie qu'on arrive pas à attraper la team supprimée
        response = self.client.get("/post/%d/"%user1_team_id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    # on vérifie qu'on ne peut pas supprimer une team appartenant à un autre utilisateur
    def test_delete_other_coach_team_forbidden(self):
        user2_team_id = Team.objects.filter(user__username="admin").first().id
        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.delete(team_root+"%d/"%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    on vérifi qu'un admin peut supprimer n'importe quelle team

    def test_delete_any_team_as_admin_success(self):
        # on se connecte en tant qu'admin
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        team_num = Team.objects.all().count()

        # on vérifie que l'on peut supprimer n'importe quelle team lorsqu'on est admin
        user2_team_id = Team.objects.filter(user__username="user2").first().id
        response = self.client.delete(team_root+"%i/"%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # on vérifie la suppression du post : on vérifie que le comptage des team a diminiué
        team_num_after_delete = Team.objects.all().count()
        self.assertEqual(team_num_after_delete,team_num-1)

        # enfin on vérifie que l'on arrive pas attraper la team détruite
        response = self.client.get(team_root+"%i/"%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)



    test de mise à jour de l'équipe

    def test_team_update(self):

        # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour la team
        user1_team_id = Team.objects.filter(user__username="john_doe",status=3).first().id
        user2_team_id = Team.objects.filter(user__username="user2",status=3).first().id
        admin_team_id = Team.objects.filter(user__username="admin",status=3).first().id

        # un appel anonyme ne doit pas pouvoir mettre à jour une team
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on connecte un utilisateur
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on vérifie qu'un utilisateur a bien le droit de mettre à jour ses données
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        #on vérifie que la mise à jour est bien faite
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["nb_rerolls"],update_datas["nb_rerolls"])
        self.assertEqual(response.data["pop"],update_datas["pop"])
        self.assertEqual(response.data["assistants"],update_datas["assistants"])
        self.assertEqual(response.data["cheerleaders"],update_datas["cheerleaders"])
        self.assertEqual(response.data["apo"],update_datas["apo"])
        self.assertEqual(response.data["DungeonBowl"],update_datas["DungeonBowl"])
        # une team dont le status est à 3 doit passer à 1
        self.assertEqual(response.data["status"],1)

        user1_team_id = Team.objects.filter(user__username="john_doe",status=0).first().id
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        # une team dont le status est à 0 doit passer à 1
        self.assertEqual(response.data["status"],1)

        # on vérifie qu'on ne peut pas mettre à jour une team d'un autre utilisateur
        response = self.client.put(team_root+"%d/"%admin_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie qu'un admin peut mettre à jour n'importe quelle team
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.put(team_root+"%d/"%user2_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie qu'un admin ne peut pas mettre à jour une équipe dont le status est 1 ou 2
        user1_team_id = Team.objects.filter(user__username="john_doe",status=1).first().id
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        user1_team_id = Team.objects.filter(user__username="john_doe",status=2).first().id
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)



    test de mis à jour partiel

    def test_post_partial_update(self):
         # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour le post
        user1_team_id = Team.objects.filter(user__username="john_doe",status=3).first().id
        admin_team_id = Team.objects.filter(user__username="admin",status=3).first().id

        # on vérifie qu'une team ne peut pas être mise à jour par un utilisateur anonyme
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on vérifie qu'un utilisateur ne peut pas mettre à jour d'autre team que la sienne
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.patch(team_root+"%d/"%admin_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie que la mise à jour d'une équipe dont le status est 1 ou 2 ne peut pas être mise à jour
        user1_team_id = Team.objects.filter(user__username="john_doe",status=1).first().id
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        user1_team_id = Team.objects.filter(user__username="john_doe",status=2).first().id
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on vérifie la bonne mise à jour de l'équipe
        user1_team_id = Team.objects.filter(user__username="john_doe",status=3).first().id
        team_user_1 = Team.objects.get(user__username="john_doe",status=3)
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["nb_rerolls"],4)
        self.assertEqual(response.data["pop"],team_user_1.pop)
        self.assertEqual(response.data["assistants"],team_user_1.assistants)
        self.assertEqual(response.data["cheerleaders"],team_user_1.cheerleaders)
        self.assertEqual(response.data["apo"],team_user_1.apo)
        self.assertEqual(response.data["DungeonBowl"],team_user_1.DungeonBowl)

        # on vérifie qu'un admin peut mettre à jour partiellement une équipe
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        user1_team_id = Team.objects.filter(user__username="user2",status=3).first().id
        team_user_2 = Team.objects.get(user__username="user2",status=3)
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"apo": True})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["nb_rerolls"],team_user_2.nb_rerolls)
        self.assertEqual(response.data["pop"],team_user_1.pop)
        self.assertEqual(response.data["assistants"],team_user_1.assistants)
        self.assertEqual(response.data["cheerleaders"],team_user_1.cheerleaders)
        self.assertEqual(response.data["apo"],True)
        self.assertEqual(response.data["DungeonBowl"],team_user_1.DungeonBowl)
"""
