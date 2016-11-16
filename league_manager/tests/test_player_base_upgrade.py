__author__ = 'Bertrand'


from rest_framework.test import APITestCase
from rest_framework import status
from league_manager.tests.factories.player_upgrade_factories import PlayerUpgradeFactory
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.team import Team
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.player import Player
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from league_manager.tests.factories.team_factories import TeamFactory
from league_manager.tests.factories.player_factories import PlayerFactory
from league_manager.tests.datas.input.player_base_upgrade import *

upb_root="/player_base_upgrade/publish/"

"""
On teste le mécanisme d'ajout d'upgrade de base
"""
class TestPlayerBaseUpgrade(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def create_context(self):
        # on crée le contexte
        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_valid_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl2.id,"value": 1,"skill" : 74},
        ]

        return publish_valid_upgrade

    """
     On vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
    """
    def test_publish_base_upgrade_anonymous_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_upgrade)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
     On vérifie qu'un utilisateur ne peut pas publier un upgrade d'un autre joueur
    """
    def test_publish_other_coach_base_upgrade_rejected(self):
        publish_valid_upgrade = self.create_context()

        myuser2 = UserFactory.create(username = "user2")
        self.client.force_authenticate(user=myuser2)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_valid_upgrade)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     On vérifie qu'un admin peut publier n'importe quel upgrade
    """
    def test_publish_admin_uprade(self):
        publish_valid_upgrade = self.create_context()

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myadmin)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_valid_upgrade)

        #on vérifie que la réponse est OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les compétences ont été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_valid_upgrade[0]['player_id'],pk=3).count(),1)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_valid_upgrade[1]['player_id'],pk=74).count(),1)

        # on ne fait pas davantage de vérifications, car les test d'upgrade couvrent la publication

    """
     On vérifie qu'une publication par un utilisateur normal est ok
    """
    def test_publish_normal_user(self):
        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_valid_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl3.id,"value": 0,"skill" : 3},
            {'player_id':pl2.id,"value": 1,"skill" : 74},
        ]

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myuser)

        # on vérifie que la publication est OK
        response = self.client.post(upb_root,data=publish_valid_upgrade)

        #on vérifie que la réponse est OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les compétences ont été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_valid_upgrade[0]['player_id'],pk=3).count(),1)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_valid_upgrade[1]['player_id'],pk=3).count(),1)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_valid_upgrade[2]['player_id'],pk=74).count(),1)

        # il faut vérifier que l'équipe a été publiée
        self.assertEqual(team1.status,1)

        # on ne fait pas davantage de vérifications, car les test d'upgrade couvrent la publication

    """
     On vérifie qu'il est impossible de publier 4 upgrade, dont un double, sur une même équipe
    """
    def test_publish_4_base_upgrade_rejected(self):
        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_4_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl3.id,"value": 0,"skill" : 3},
            {'player_id':pl4.id,"value": 1,"skill" : 74},
            {'player_id':pl2.id,"value": 0,"skill" : 3},
        ]

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myuser)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_4_upgrade)

        #on vérifie que la réponse est KO
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que les compétences n'ont pas été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_4_upgrade[0]['player_id'],pk=3).count(),0)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_4_upgrade[1]['player_id'],pk=74).count(),0)

        # on ne fait pas davantage de vérifications, car les test d'upgrade couvrent la publication

    """
     On vérifie qu'il est impossible de publier 2 upgrade de base sur le même joueur
    """
    def test_publish_2_base_upgrade_on_same_player_rejected(self):
        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_2_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl1.id,"value": 0,"skill" : 5},
        ]

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myuser)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_2_upgrade)

        #on vérifie que la réponse est KO
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que les compétences n'ont pas été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_2_upgrade[0]['player_id'],pk=3).count(),0)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_2_upgrade[1]['player_id'],pk=5).count(),0)

        # on ne fait pas davantage de vérifications, car les test d'upgrade couvrent la publication

    """
     On vérifie qu'il est impossible de publier un upgrade d'augmentation de stats
    """
    def test_publish_stats_base_upgrade_rejected(self):
        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_2_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl2.id,"value": 3,"skill" : 3},
        ]

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myuser)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_2_upgrade)

        #on vérifie que la réponse est KO
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que les compétences n'ont pas été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_2_upgrade[0]['player_id'],pk=3).count(),0)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_2_upgrade[1]['player_id'],pk=5).count(),0)

    """
     On vérifie qu'il est impossible de publier 2 doubles sur une même équipe
    """
    def test_publish_2_doubles_rejected(self):

        myuser = UserFactory.create()

        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl2 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl3 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))
        pl4 = PlayerFactory.create(team=team1, ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        publish_4_upgrade=[
            #blocage
            {'player_id':pl1.id,"value": 0,"skill" : 3},
            {'player_id':pl4.id,"value": 1,"skill" : 74},
            {'player_id':pl2.id,"value": 1,"skill" : 73},
        ]

        myadmin = AdminFactory.create()
        self.client.force_authenticate(user=myuser)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.post(upb_root,data=publish_4_upgrade)

        #on vérifie que la réponse est KO
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que les compétences n'ont pas été ajoutées au joueurs
        self.assertEqual(Ref_Skills.objects.filter(player=publish_4_upgrade[0]['player_id'],pk=3).count(),0)
        self.assertEqual(Ref_Skills.objects.filter(player=publish_4_upgrade[1]['player_id'],pk=74).count(),0)















