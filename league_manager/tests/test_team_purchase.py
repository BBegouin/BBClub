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
from league_manager.tests.datas.input.team_purchase import *
from django.contrib.auth.models import User

team_purchase_root="/team/%i/purchase/"

"""
"""
class TestTeamPurchase(APITestCase):

    @classmethod
    def setUpTestData(cls):
       pass

    """
     Test d'achat par un utilisateur anyonyme interdit
    """
    def test_anonymous_purchase_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        # on vérifie qu'un utilisateur non identifié ne peut pas réaliser un achat
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
     Test d'achat sur une équipe d'un autre coach interdit
    """
    def test_other_coach_purchase_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        myuser2 = UserFactory.create(username = "user2")
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser2)

        # on vérifie qu'un utilisateur ne peut pas réaliser un achat sur une équipe qui n'est pas la sienne
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat sur une équipe draft interdit
    """
    def test_purchase_on_draft_team_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=0)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        # on vérifie qu'un utilisateur ne peut pas réaliser un achat sur une équipe qui n'est pas la sienne
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat sur sa propre équipe avec montant trop élevé : interdit
    """
    def test_purchase_too_expensive_rejected(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        # la team de base à 10k de tréso, on essaye d'acheter 3 joueurs, ça devrait pas bien se passer...
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on teste quand y a trop de rr
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_too_much_rr)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on teste quand y a trop d'assistants
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_too_much_assistants)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on teste quand y atrop de pompom
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_too_much_cheerleaders)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        # on crée les journeymens pour le test "quand il ya trop de journeymens"
        jm1 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=15),
                                    is_journeyman = True)
        jm2 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=14),
                                    is_journeyman = True)


        team_purchase_journeymens={
            "journeymens": [
                { "player_id" : jm1.id,},
                { "player_id" : jm2.id,},
            ],
        }
        #on teste quand y a trop de journeymens
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_journeymens)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on teste quand y a trop de tout
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_all)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat de joueurs non compatibles avec l'équipe : interdit
    """
    def test_purchase_non_compatible_players_rejected(self):
        myuser = UserFactory.create()
        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        # la team de base à 10k de tréso, on essaye d'acheter 3 joueurs, ça devrait pas bien se passer...
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_forbiddens_players)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat de journeymens inconnus : interdit
    """
    def test_purchase_unknown_journeymens_rejected(self):
        myuser = UserFactory.create()
        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        # On essaye d'acheter des journeymens parfaitement inconnus au bataillon
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_unknown_journeymens)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat de journeymens d'une autre équipe : interdit
    """
    def test_purchase_other_coach_journeymens_rejected(self):
        myuser = UserFactory.create()
        myuser2 = UserFactory.create(username = "user2")

        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)
        team2 = TeamFactory.create(user=myuser2,status=1,treasury=2000)

        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        jm1 = PlayerFactory.create( team=team2,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=15),
                                    is_journeyman = True)
        jm2 = PlayerFactory.create( team=team2,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=14),
                                    is_journeyman = True)

        team_purchase_journeymens={
            "journeymens": [
                { "player_id" : jm1.id,},
                { "player_id" : jm2.id,},
            ],
        }

        # On essaye d'acheter les journeymens de l'équipe 2 sur l'équipe 1, ça va pas bien se passer
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_journeymens)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat de joueurs interdit si l'équipe à 16 joueurs
    """
    def test_purchase_too_many_players_rejected(self):
        myuser = UserFactory.create()

        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)

        # on crée une équipe avec 14 joueurs
        for i in range(0,14):
            PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser)

        # On essaye d'acheter 3 joueurs, ce qui nous ferait passer à 17 joueurs
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     Test d'achat de joueurs valide :
     on vérifie la mise à jour du TV ainsi que le nombre de journaliers
    """
    def test_purchase_players_successful(self):
        myuser = UserFactory.create()

        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)

        # on crée une équipe avec 11, dont deux journaliers joueurs
        for i in range(0,9):
            PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        jm1 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13),
                                    is_journeyman = True)
        jm2 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13),
                                    is_journeyman = True)
        team1.update_TV()
        tv1 = team1.TV
        treso1 = team1.treasury
        self.client.force_authenticate(user=myuser)

        # On achète effectivement les joueurs
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_player)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        t = Team.objects.get(pk=team1.id)
        # on vérifie que le TV de la team est monté de 230 et a baissé de 120, car on a viré les journaliers donc +110
        self.assertEqual(tv1+110,t.TV)

        #on vérifie que les deux joueurs ont été ajoutés à l'équipe, et on vérifie que les journaliers ont été
        # supprimés
        nb_journeymens = Player.objects.filter(team = team1,is_journeyman = True).count()
        self.assertEqual(nb_journeymens,0)

        #on vérifie que la trésorerie a baissé de 230
        treso2 = Team.objects.get(pk = team1.id).treasury
        self.assertEqual(treso1-230,treso2)


    """
     Test d'achat de rr valide :
     on vérifie qu'il faut bien payer le double du prix de la RR
     on vérifie la mise à jour du TV
    """
    def test_purchase_reroll_successful(self):
        myuser = UserFactory.create()

        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)

        # on crée une équipe avec 11, dont deux journaliers joueurs
        for i in range(0,9):
            PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        jm1 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13),
                                    is_journeyman = True)
        jm2 = PlayerFactory.create( team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=13),
                                    is_journeyman = True)
        team1.update_TV()
        nb_rr = team1.nb_rerolls
        tv1 = team1.TV
        treso1 = team1.treasury
        self.client.force_authenticate(user=myuser)

        # On achète effectivement les joueurs
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_rr)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        t = Team.objects.get(pk=team1.id)
        # on vérifie que le TV de la team est monté de 50, car on a acheté une RR
        self.assertEqual(tv1+50,t.TV)

        #on vérifie que le nombre de rr a augmenté
        updated_rr = Team.objects.get(pk = team1.id).nb_rerolls
        self.assertEqual(nb_rr+1,updated_rr)

        #on vérifie que la trésorerie a baissé de 100
        treso2 = Team.objects.get(pk = team1.id).treasury
        self.assertEqual(treso1-100,treso2)

    """
     Test d'achat d'assistants et de pom-pom
     on vérifie la mise à jour du TV
    """
    def test_purchase_team_stuff_successful(self):
        myuser = UserFactory.create()

        # on crée une team avec de la tréso, pour que cela ne bloque pas l'achat
        team1 = TeamFactory.create(user=myuser,status=1,treasury=2000)

        # on crée une équipe avec 11, dont deux journaliers joueurs
        for i in range(0,9):
            PlayerFactory.create(team=team1,
                                 ref_roster_line = Ref_Roster_Line.objects.get(pk=13))

        team1.update_TV()
        nb_rr = team1.nb_rerolls
        tv1 = team1.TV
        treso1 = team1.treasury
        nb_ass = team1.assistants
        nb_cheer = team1.cheerleaders
        apo = team1.apo
        self.client.force_authenticate(user=myuser)

        # On achète effectivement les joueurs
        response = self.client.patch(team_purchase_root%team1.id,team_purchase_all)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        t = Team.objects.get(pk=team1.id)
        # on vérifie que le TV de la team est monté de 370, car on a acheté une RR
        self.assertEqual(tv1+370,t.TV)

        #on vérifie que le nombre de rr a augmenté
        updated_rr = Team.objects.get(pk = team1.id).nb_rerolls
        self.assertEqual(nb_rr+1,updated_rr)

        #on vérifie que le nombre d'assistants a augmenté
        updated_ass = Team.objects.get(pk = team1.id).assistants
        self.assertEqual(nb_ass+2,updated_ass)

        #on vérifie que le nombre de cheerleaders a augmenté
        updated_cheer = Team.objects.get(pk = team1.id).cheerleaders
        self.assertEqual(nb_cheer+3,updated_cheer)

        #on vérifie qu'on a un apo a augmenté
        apo = Team.objects.get(pk = team1.id).apo
        self.assertEqual(apo,True)

        #on vérifie que la trésorerie a baissé de 420
        treso2 = Team.objects.get(pk = team1.id).treasury
        self.assertEqual(treso1-420,treso2)

