__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.league import League
from league_manager.models.team import Team,Player
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.team_factories import TeamFactory
from league_manager.tests.factories.player_factories import PlayerFactory
from league_manager.tests.datas.input.team import *
from django.contrib.auth.models import User

team_root="/team/"
team_publish_root="/team/%i/publish/"
team_unpublish_root="/team/%i/unpublish/"

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestTeam(APITestCase):

    created_team_id = 0


    @classmethod
    def setUpTestData(cls):
        #on crée les utilisateurs de test
        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        Waz = UserFactory.create(username="Wazdakka",password="user2")
        Guiz = UserFactory.create(username="Guizmo",password="user2")
        myadmin = AdminFactory.create()

        #on crée les équipes de test
        team1 = TeamFactory.create( user=Waz,
                                    status=1,
                                    name="CAPT",
                                    ref_roster = Ref_Roster.objects.get(name="Humains"),
                                    league = League.objects.first(),
                                    treasury = 10,
                                    nb_rerolls = 3,
                                    pop = 4,
                                    assistants = 0,
                                    cheerleaders = 0,
                                    apo = False,
                                    icon_file_path = "icon file path",
                                    DungeonBowl = False)

        pl1 = PlayerFactory.create( team=team1,
                                    name = "num1",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=46),
                                    num = 1,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl2 = PlayerFactory.create( team=team1,
                                    name = "num2",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=44),
                                    num = 2,
                                    total_xp = 0,
                                    need_upgrade = False)
        pl3 = PlayerFactory.create( team=team1,
                                    name = "num3",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=43),
                                    num = 3,
                                    total_xp = 0,
                                    need_upgrade = False)
        pl4 = PlayerFactory.create( team=team1,
                                    name = "num4",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=43),
                                    num = 4,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl5 = PlayerFactory.create( team=team1,
                                    name = "num5",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=45),
                                    num = 5,
                                    total_xp = 0,
                                    need_upgrade = False )
        pl6 = PlayerFactory.create(team=team1,
                                    name = "num6",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=45),
                                    num = 6,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl7 = PlayerFactory.create(team=team1,
                                    name = "num7",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=45),
                                    num = 7,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl8 = PlayerFactory.create( team=team1,
                                    name = "num8",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=45),
                                    num = 8,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl9 = PlayerFactory.create( team=team1,
                                    name = "num9",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=42),
                                    num = 9,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl10 = PlayerFactory.create(team=team1,
                                    name = "num10",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=42),
                                    num = 10,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl11 = PlayerFactory.create(team=team1,
                                    name = "num11",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=42),
                                    num = 11,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl12 = PlayerFactory.create(team=team1,
                                    name = "num12",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=42),
                                    num = 12,
                                    total_xp = 0,
                                    need_upgrade = False)

        team12 = TeamFactory.create(user=myuser,status=1)
        team12 = TeamFactory.create(user=myuser,status=0)
        team2 = TeamFactory.create(user=user2,status=1)
        team3 = TeamFactory.create(user=user2,status=0)
        team4 = TeamFactory.create(user=myadmin,status=1)
        team5 = TeamFactory.create(user=myadmin,status=0)



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


    """
     Test de récupération d'une équipe
    """
    def test_team_detail_success(self):
        
        team_id = Team.objects.filter(user__username="wazdakka").first().id
        response = self.client.get(team_root+"%i/"%team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #il faut tester le retour pour assurer la stabilité des interfaces, mais v'la la structure...


    """
     Test de récupération de la liste des team
    """
    def test_team_list_success(self):

        # on test la récupération simple
        response = self.client.get(team_root)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        team_cpt = Team.objects.count()
        self.assertEqual(len(response.data),team_cpt)


    """
     Test de récupèration des équipes d'un coach
    """
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

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on lance la création d'une équipe
        response = self.client.post(team_root,data=create_datas_wrong_player)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


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


    """
     on vérifie que l'utilisateur connecté a bien le droit de supprimer une de ses propres team
    """
    def test_delete_team_success(self):

        team_num = Team.objects.all().count()
        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        # on vérifie qu'on a le droit de supprimer une de ses propres team
        user1_team_id = Team.objects.filter(user__username="john_doe").last().id
        response = self.client.delete(team_root+"%d/"%user1_team_id)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # on vérifie la suppression du post : on vérifie que le comptage des team a diminiué
        team_num_after_delete = Team.objects.all().count()
        self.assertEqual(team_num_after_delete,team_num-1)

        # On vérifie qu'on arrive pas à attraper la team supprimée
        response = self.client.get("/post/%d/"%user1_team_id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    """
     on vérifie qu'on ne peut pas supprimer une team appartenant à un autre utilisateur
    """
    def test_delete_other_coach_team_forbidden(self):

        user2_team_id = Team.objects.filter(user__username="admin").first().id
        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.delete(team_root+"%d/"%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    """
     on vérifie qu'un admin peut supprimer n'importe quelle team
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
    test de publication d'une équipe
    """
    def test_team_publish(self):

        user2_team_id = Team.objects.filter(user__username="john_doe",status="0").first().id

        self.client.force_authenticate()

        # on vérifie qu'un utilisateur anonyme ne pas publier une équipe
        response = self.client.patch(team_publish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on vérifie qu'un utilisateur ne peut publier que ses équipes
        self.client.force_authenticate(user=User.objects.get(username="wazdakka"))
        response = self.client.patch(team_publish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on vérifie que la publication est fonctionnelle par un admin
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        response = self.client.patch(team_publish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie que la publication par un utilisateur est fonctionnelle
        self.client.force_authenticate(user=User.objects.get(username="user2"))
        user2_team_id = Team.objects.filter(user__username="user2",status="0").first().id
        response = self.client.patch(team_publish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    """
    test de dépublication d'une équipe
    """
    def test_team_unpublish(self):

        user2_team_id = Team.objects.filter(user__username="john_doe",status="1").first().id

        self.client.force_authenticate()

        # on vérifie qu'un utilisateur anonyme ne pas publier une équipe
        response = self.client.patch(team_unpublish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on vérifie qu'un utilisateur ne peut publier que ses équipes
        self.client.force_authenticate(user=User.objects.get(username="wazdakka"))
        response = self.client.patch(team_unpublish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on vérifie que la publication est fonctionnelle par un admin
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        response = self.client.patch(team_unpublish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie que la publication par un utilisateur est fonctionnelle
        self.client.force_authenticate(user=User.objects.get(username="user2"))
        user2_team_id = Team.objects.filter(user__username="user2",status="1").first().id
        response = self.client.patch(team_unpublish_root%user2_team_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie qu'il est impossible de dépublier une team qui a déjà des matchs
        # TBD


    """
    test de mise à jour de l'équipe
    """
    def test_team_update(self):

        # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour la team
        user1_team_id = Team.objects.filter(user__username="john_doe",status=0).first().id
        user2_team_id = Team.objects.filter(user__username="user2",status=0).first().id
        admin_team_id = Team.objects.filter(user__username="admin",status=0).first().id

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

        user1_team_id = Team.objects.filter(user__username="john_doe",status=0).first().id
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)

        # on vérifie qu'on ne peut pas mettre à jour une team d'un autre utilisateur
        response = self.client.put(team_root+"%d/"%admin_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie qu'un admin peut mettre à jour n'importe quelle team
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.put(team_root+"%d/"%user2_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie qu'un admin ne peut pas mettre à jour une équipe dont le status n'est pas 0
        user1_team_id = Team.objects.filter(user__username="john_doe",status=1).first().id
        response = self.client.put(team_root+"%d/"%user1_team_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)


    """
     test de mis à jour partiel
    """
    def test_post_partial_update(self):

         # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour le post
        user1_team_id = Team.objects.filter(user__username="john_doe",status=0).first().id
        admin_team_id = Team.objects.filter(user__username="admin",status=0).first().id

        # on vérifie qu'une team ne peut pas être mise à jour par un utilisateur anonyme
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on vérifie qu'un utilisateur ne peut pas mettre à jour d'autre team que la sienne
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.patch(team_root+"%d/"%admin_team_id,{"nb_rerolls": 4})
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie la bonne mise à jour de l'équipe
        team_user_1 = Team.objects.get(pk=user1_team_id)
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
        user1_team_id = Team.objects.filter(user__username="user2",status=0).first().id
        team_user_2 = Team.objects.filter(user__username="user2",status=0).first()
        response = self.client.patch(team_root+"%d/"%user1_team_id,{"apo": True})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["nb_rerolls"],team_user_2.nb_rerolls)
        self.assertEqual(response.data["pop"],team_user_1.pop)
        self.assertEqual(response.data["assistants"],team_user_1.assistants)
        self.assertEqual(response.data["cheerleaders"],team_user_1.cheerleaders)
        self.assertEqual(response.data["apo"],True)
        self.assertEqual(response.data["DungeonBowl"],team_user_1.DungeonBowl)

    """
    On vérifie que la méthode d'ajout / suppression des journeymens fonctionne correctement
    """
    def test_update_journey_mens(self):
        #on crée les utilisateurs de test
        test = UserFactory.create(username="test",password="test")

        #on crée une équipe de test complète
        team1 = TeamFactory.create( user=test,
                                    status=1,
                                    ref_roster = Ref_Roster.objects.get(name="Nordiques"),
                                    league = League.objects.first(),
                                    treasury = 10,
                                    nb_rerolls = 3,
                                    pop = 4,
                                    assistants = 0,
                                    cheerleaders = 0,
                                    apo = False,
                                    icon_file_path = "icon file path",
                                    DungeonBowl = False)

        pl1 = PlayerFactory.create( team=team1,
                                    name = "num1",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=70),
                                    num = 1,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl2 = PlayerFactory.create( team=team1,
                                    name = "num2",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=70),
                                    num = 2,
                                    total_xp = 0,
                                    need_upgrade = False)
        pl3 = PlayerFactory.create( team=team1,
                                    name = "num3",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=70),
                                    num = 3,
                                    total_xp = 0,
                                    need_upgrade = False)
        pl4 = PlayerFactory.create( team=team1,
                                    name = "num4",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=70),
                                    num = 4,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl5 = PlayerFactory.create( team=team1,
                                    name = "num5",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=70),
                                    num = 5,
                                    total_xp = 0,
                                    need_upgrade = False )
        pl6 = PlayerFactory.create(team=team1,
                                    name = "num6",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=71),
                                    num = 6,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl7 = PlayerFactory.create(team=team1,
                                    name = "num7",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=72),
                                    num = 7,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl8 = PlayerFactory.create( team=team1,
                                    name = "num8",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=72),
                                    num = 8,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl9 = PlayerFactory.create( team=team1,
                                    name = "num9",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=73),
                                    num = 9,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl10 = PlayerFactory.create(team=team1,
                                    name = "num10",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=73),
                                    num = 10,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl11 = PlayerFactory.create(team=team1,
                                    name = "num11",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=74),
                                    num = 11,
                                    total_xp = 0,
                                    need_upgrade = False)

        pl12 = PlayerFactory.create(team=team1,
                                    name = "num12",
                                    miss_next_game = False,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=75),
                                    num = 12,
                                    total_xp = 0,
                                    need_upgrade = False)

        team1.update_TV()
        # on met à jour le compte des journey mens
        team1.update_Journeymen()

        # on vérifie qu'aucun journeymens n'a été crée
        self.assertEqual(Player.objects.filter(team=team1,is_journeyman=True).count(),0)

        #au passage on vérifie le TV
        self.assertEqual(Team.objects.get(pk=team1.id).TV,1150)

        #on blesse certains joueurs, et on voit si les journeymens sont crés
        pl12.miss_next_game = True
        pl12.save()
        pl11.miss_next_game = True
        pl11.save()
        pl10.miss_next_game = True
        pl10.save()

        # on met à jour le compte des journey mens
        team1.update_Journeymen()

        #2 journeymens doivent être crée
        self.assertEqual(Player.objects.filter(team=team1,is_journeyman=True).count(),2)
        self.assertEqual(Player.objects.filter(team=team1,miss_next_game=False).count(),11)

        team1.update_TV()
        self.assertEqual(Team.objects.get(pk=team1.id).TV,910)

        #on répare certains des joueurs blessés
        pl12.miss_next_game = False
        pl12.save()

        team1.update_Journeymen()

        #on doit avoir supprimé un jm
        self.assertEqual(Player.objects.filter(team=team1,is_journeyman=True).count(),1)

