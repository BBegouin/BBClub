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
from league_manager.tests.datas.input.player_upgrade import *


up_publish_root="/player_upgrade/%i/publish/"

"""
"""
class TestPlayerUpgrade(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    """
     On vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
    """
    def test_publish_upgrade_anonymous_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.patch(up_publish_root%up.id,publish_upgrade_simple)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    """
     On vérifie qu'un utilisateur ne peut pas publier un upgrade d'un autre joueur
    """
    def test_publish_other_coach_rejected(self):
        # on crée le contexte
        myuser = UserFactory.create()
        myuser2 = UserFactory.create(username = "user2")
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        self.client.force_authenticate(user=myuser2)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # on vérifie qu'un utilisateur non identifié ne peut pas publier un upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_simple)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

    """
     On vérifie qu'un admin peut publier n'importe quel upgrade
    """
    def test_publish_admin_uprade(self):
        # on crée le contexte
        myuser = UserFactory.create()
        myadmin = AdminFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.init_datas()

        self.client.force_authenticate(user=myadmin)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie qu'un admin peut publier n'importe quel upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_simple)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que la skill a bien été ajoutée au joueur, en cherchant la skill dans la liste de skill du joueur
        self.assertEqual(Player.objects.get(pk=pl1.id).skills.filter(pk=publish_upgrade_simple["skill"]).count(),1)

    """
     On vérifie qu'une publication d'une skill en double est refusée
    """
    def test_publish_redundant_skill_rejected(self):
         # on crée le contexte
        myuser = UserFactory.create()
        myadmin = AdminFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.init_datas()

        self.client.force_authenticate(user=myadmin)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie qu'un admin peut publier n'importe quel upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_doublon)

        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)



    """
     On vérifie qu'un upgrade skill normal ajoute la compétence sélectionnée au joueur,
     et ajoute 2 au TV de l'équipe concernée
    """
    def test_publish_skill(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_simple)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que la skill a bien été ajoutée au joueur, en cherchant la skill dans la liste de skill du joueur
        self.assertEqual(Player.objects.get(pk=pl1.id).skills.filter(pk=publish_upgrade_simple["skill"]).count(),1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+20,tv2)

    """
     On vérifie qu'on refuse l'ajout de compétence non autorisée :
      - double si upgrade simple
      - compétence hors liste
    """
    def test_publish_upgrade_with_forbidden_skill_rejected(self):
        # on vérifie qu'on refuse la publication d'une double si l'upgrade est simple
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # on essaye de publier une double avec un upgrade simple
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_simple_refused)

        # on se fait jeter
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que l'upgrade n'a pas bougé
        self.assertEqual(up,PlayerUpgrade.objects.get(pk=up.id))

        # on essaye de publier une ext avec un upgrade double
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_double_refused)

        # on se fait jeter
        self.assertEqual(response.status_code,status.HTTP_406_NOT_ACCEPTABLE)

        #on vérifie que l'upgrade n'a pas bougé
        self.assertEqual(up,PlayerUpgrade.objects.get(pk=up.id))

        #on vérifie que le joueur n'a toujours que deux skills
        self.assertEqual(Ref_Skills.objects.filter(player=pl1).count(),2)

        #on vérifie que le TV de l'équipe n'a pas bougé
        self.assertEqual(tv1,Team.objects.get(pk=team1.id).TV)

    """
     On vérifie que l'ajout d'une compétence double est ajoutée au joueur
     et ajoute 3 au TV de l'équipe concernée
    """
    def test_publish_double_skill(self):
         # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_double)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que la skill a bien été ajoutée au joueur, en cherchant la skill dans la liste de skill du joueur
        self.assertEqual(Player.objects.get(pk=pl1.id).skills.filter(pk=publish_upgrade_double["skill"]).count(),1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+30,tv2)

    """
     On vérifie que l'ajout d'un point de M est ajoutée au joueur
     et ajoute 3 au TV de l'équipe concernée
    """
    def test_publish_M(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()
        M1 = pl1.M

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_M)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les stats du joueurs ont bien été mises à jour
        self.assertEqual(Player.objects.get(pk=pl1.id).M,M1+1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+30,tv2)

    """
     On vérifie que l'ajout d'un point de Ar est ajoutée au joueur
     et ajoute 3 au TV de l'équipe concernée
    """
    def test_publish_Ar(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()
        AR1 = pl1.Ar

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_Ar)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les stats du joueurs ont bien été mises à jour
        self.assertEqual(Player.objects.get(pk=pl1.id).Ar,AR1+1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+30,tv2)

    """
     On vérifie que l'ajout d'un point de Ag est ajoutée au joueur
     et ajoute 4 au TV de l'équipe concernée
    """
    def test_publish_Ag(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()
        AG1 = pl1.Ag

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_Ag)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les stats du joueurs ont bien été mises à jour
        self.assertEqual(Player.objects.get(pk=pl1.id).Ag,AG1+1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+40,tv2)

    """
     On vérifie que l'ajout d'un point de F est ajoutée au joueur
     et ajoute 5 au TV de l'équipe concernée
    """
    def test_publish_F(self):
        # on crée le contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        team1.update_TV()
        tv1 = team1.TV
        pl1.init_datas()
        F1 = pl1.F

        self.client.force_authenticate(user=myuser)

        # on crée un upgrade qui reste à être publié
        up = PlayerUpgradeFactory.create(player=pl1)

        # On vérifie que le proprio peut publier l'upgrade
        response = self.client.patch(up_publish_root%up.id,data=publish_upgrade_F)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie que les stats du joueurs ont bien été mises à jour
        self.assertEqual(Player.objects.get(pk=pl1.id).F,F1+1)

        # on vérifie que le TV a bien été mis à jour
        tv2 = Team.objects.get(pk=team1.id).TV

        self.assertEqual(tv1+50,tv2)













