__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase,APITransactionTestCase
from league_manager.models.team import Team,Player
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.team_factories import TeamFactory
from rest_framework.authtoken.models import Token
from league_manager.tests.datas.team_datas import *
from django.contrib.auth.models import User

team_root="/team/"

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestTeam(APITestCase):

    @classmethod
    def setUpTestData(cls):
        #on crée les utilisateurs de test
        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        myadmin = AdminFactory.create()

        TeamFactory.create(user=myuser,status=0)
        TeamFactory.create(user=myuser,status=1)
        TeamFactory.create(user=myuser,status=2)
        TeamFactory.create(user=myuser,status=3)
        TeamFactory.create(user=user2)
        TeamFactory.create(user=user2)
        TeamFactory.create(user=user2,status=3)
        TeamFactory.create(user=myadmin,status=3)
        TeamFactory.create(user=myadmin,status=0)
        #on crée les équipes de test

        # on crée également les tokens afin que les utilisateurs puissent se loguer
        Token.objects.create(user=myuser).save()
        Token.objects.create(user=user2).save()
        Token.objects.create(user=myadmin).save()

    """

     Test de récupération d'une équipe

    """
    def test_team_detail_success(self):
        team_id = Team.objects.all().first().id
        response = self.client.get(team_root+"%i/"%team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    """

     Test de récupération de la liste des post

    """
    def test_team_list_success(self):
        # on test la récupération simple
        response = self.client.get(team_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        team_cpt = Team.objects.count()
        self.assertEqual(len(response.data),team_cpt)

    def test_team_list_for_coach_success(self):

        # si on fait une requête avec le param coach, on doit avoir les équipes du coach
        admin_id = User.objects.get(username="admin").id
        response = self.client.get(team_root+"?coach=%i"%admin_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on compte le nombre d'équipe en BDD
        admin_team_cpt = Team.objects.filter(user__username="admin").count()
        # on vérifie que le nombre d'équipe récupéré correspond a celui en BDD
        self.assertEqual(len(response.data),admin_team_cpt)

    """
     Test de création d'une équipe : création anonyme interdite
    """
    def test_create_team_anonymous_forbidden(self):
        response = self.client.post(team_root,data=create_datas)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
     Test de création d'une équipe : création autorisée et correct
    """
    def test_create_team_success(self):
        #on sauvegarde le nombre d'article avant la création
        Team_num = Team.objects.count()

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'une équipe
        response = self.client.post(team_root,data=create_datas)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # on vérifie que la team est bien crée
        created_team_id = response.data["id"]
        created_team = Team.objects.get(pk=created_team_id)
        # on vérifie que le nombre de team a augmenté
        self.assertEqual(Team.objects.all().count(),Team_num+1)
        self.assertEqual(created_team.name,create_datas["name"])
        self.assertEqual(created_team.ref_roster.id,create_datas["ref_roster"])
        self.assertEqual(created_team.league.id,create_datas["league"])
        self.assertEqual(created_team.treasury,create_datas["treasury"])
        self.assertEqual(created_team.nb_rerolls,create_datas["nb_rerolls"])
        self.assertEqual(created_team.pop,create_datas["pop"])
        self.assertEqual(created_team.assistants,create_datas["assistants"])
        self.assertEqual(created_team.cheerleaders,create_datas["cheerleaders"])
        self.assertEqual(created_team.apo,create_datas["apo"])
        self.assertEqual(created_team.user.id,create_datas["user"])
        self.assertEqual(created_team.icon_file_path,create_datas["icon_file_path"])
        self.assertEqual(created_team.DungeonBowl,create_datas["DungeonBowl"])

        # on vérifie que le nombre de joueurs crées dans l'équipe est le bon
        player_number = Player.objects.filter(team=created_team_id).count()
        self.assertEqual(player_number,len(create_datas["players"]))


    """
     Test de création d'une équipe : création d'une équipe trop chère interdite
    """
    #il faut également vérifier que seule une team qui respecte les starting rules peut être crée
    def test_create_team_too_expensive_forbidden(self):
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'une équipe
        response = self.client.post(team_root,data=create_datas_too_expensive)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


    """
     Test de création d'une équipe : création d'une équipe trop chère interdite
    """
    #il faut également vérifier que seule une team qui contient des joueurs de son roster puisse être crée
    def test_create_team_with_wrong_players_forbidden(self):
        #TBD
        self.assertTrue(True)

    """
     Test de suppression : suppression en masse interdite
    """
    def test_delete_all_team_forbidden(self):
        # on vérifie qu'on ne peut pas faire de suppression en masse
        response = self.client.delete(team_root)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="admin"))
        # on vérifie qu'on ne peut pas faire de suppression en masse, même loggué en admin
        response = self.client.delete(team_root)
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)


    """
     Test de suppression d'une équipe : suppression anonyme interdite
    """
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

    """
    on vérifi qu'un admin peut supprimer n'importe quelle team
    """
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


    """

    test de mise à jour de l'équipe

    """
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


    """
    test de mis à jour partiel
    """
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

