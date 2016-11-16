__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from league_manager.models.team import Team,Player
from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.tests.factories.player_upgrade_factories import PlayerUpgradeFactory
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.ref_skills import Ref_Skills
from bbc_user.tests.factories.user_factory import UserFactory
from league_manager.tests.factories.team_factories import TeamFactory
from league_manager.tests.factories.match_report_factories import MatchReportFactory
from league_manager.tests.factories.match_report_factories import TeamReportFacory,PlayerReportFactory
from league_manager.tests.datas.output.player import *
from league_manager.tests.factories.player_factories import PlayerFactory
from django.core.exceptions import ObjectDoesNotExist


"""
"""
class TestPlayers(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    """
     On vérifie l'application les upgrade lorsque l'on applique les upgrades
    """
    def test_update_stats_with_upgrade(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_stats()

        # on vérifie que les stats sont ok
        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,7)
        self.assertEqual(p.F,3)
        self.assertEqual(p.Ag,4)
        self.assertEqual(p.Ar,8)

        # on crée des upgrades et des downgrades, et on vérifie que les stats se mettent correctement à jour
        PlayerUpgradeFactory.create(value = 2,
                                        player = pl1,
                                        skill = None,
                                        status = 1)
        PlayerUpgradeFactory.create(value = 3,
                                        player = pl1,
                                        skill = None,
                                        status = 1)
        PlayerUpgradeFactory.create(value = 4,
                                        player = pl1,
                                        skill = None,
                                        status = 1)
        PlayerUpgradeFactory.create(value = 5,
                                        player = pl1,
                                        skill = None,
                                        status = 1)

        pl1.update_stats()

        # on vérifie que les stats sont ok après créations des updates
        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,8)
        self.assertEqual(p.F,4)
        self.assertEqual(p.Ag,5)
        self.assertEqual(p.Ar,9)


        # on crée un upgrade non validé, et on vérifie que cela est sans effet
        PlayerUpgradeFactory.create(value = 2,
                                        player = pl1,
                                        skill = None,
                                        status = 0)
        PlayerUpgradeFactory.create(value = 3,
                                        player = pl1,
                                        skill = None,
                                        status = 0)
        PlayerUpgradeFactory.create(value = 4,
                                        player = pl1,
                                        skill = None,
                                        status = 0)
        PlayerUpgradeFactory.create(value = 5,
                                        player = pl1,
                                        skill = None,
                                        status = 0)

        pl1.update_stats()

        # on vérifie que les stats n'ont pas bougé ok après créations des updates
        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,8)
        self.assertEqual(p.F,4)
        self.assertEqual(p.Ag,5)
        self.assertEqual(p.Ar,9)

        # on crée deux upgrade F supplèmentaires pour vérifier qu'on est maxé à 2 upgrades
        PlayerUpgradeFactory.create(value = 2,
                                        player = pl1,
                                        skill = None,
                                        status = 1)
        PlayerUpgradeFactory.create(value = 2,
                                        player = pl1,
                                        skill = None,
                                        status = 1)

        pl1.update_stats()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,9)
        self.assertEqual(p.F,4)
        self.assertEqual(p.Ag,5)
        self.assertEqual(p.Ar,9)

    """
     On vérifie que les rapports de match permettent bien de mettre à jour les stats d'un joueur
    """
    def test_update_stats_with_downgrade(self):

        # création du contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        team2 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_stats()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,7)
        self.assertEqual(p.F,3)
        self.assertEqual(p.Ag,4)
        self.assertEqual(p.Ar,8)

        # on crée un rapport de match avec juste une blessure de downgrade de par carac
        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=3,)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=4,)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=5,)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=6,)

        pl1.update_stats()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,6)
        self.assertEqual(p.F,2)
        self.assertEqual(p.Ag,3)
        self.assertEqual(p.Ar,7)

        # on crée deux rapport de downgrade de mouv, et on vérifie qu'on est capé à deux
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=3,)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=3,)

        pl1.update_stats()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,5)
        self.assertEqual(p.F,2)
        self.assertEqual(p.Ag,3)
        self.assertEqual(p.Ar,7)

    """
     On vérifie qu'une blessure est bien prise en compte,
     et qu'un match non joué remet à zéro les compteurs de blessures
    """
    def test_update_MNG(self):
        # création du contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_stats()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.M,7)
        self.assertEqual(p.F,3)
        self.assertEqual(p.Ag,4)
        self.assertEqual(p.Ar,8)

        # on crée un rapport de match avec une blessure afin de vérifier que le joueur ne jouera pas
        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=3,)

        pl1.update_mng()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.miss_next_game,True)

        # on crée un second rapport de match, le joueur doit donc désormais jouer le prochain match
        mr2 = MatchReportFactory.create()
        tr2 = TeamReportFacory.create(match=mr2,team=team1)

        pl1.update_mng()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.miss_next_game,False)

    """
     On vérifie la mise à jour de la liste des skills suite à un upgrade
    """
    def test_update_skills_with_upgrade(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_stats()
        pl1.update_skills()

        p = Player.objects.get(pk=pl1.id)
        # on vérifie que les la liste des skill corrspond à la iste des skills de base
        self.assertEqual(list(Ref_Roster_Line.objects.get(pk=16).base_skills.values_list()),list(p.skills.values_list()))

        # on crée 2 upgrades de skills, une simple, et une double
        PlayerUpgradeFactory.create(value = 1,
                                    player = pl1,
                                    skill = Ref_Skills.objects.get(name='Garde'),
                                    status = 1)
        PlayerUpgradeFactory.create(value = 1,
                                    player = pl1,
                                    skill = Ref_Skills.objects.get(name='Esquive'),
                                    status = 1)

        pl1.update_skills()

        p = Player.objects.get(pk=pl1.id)
        # on vérifie que les upgrades sont bien present
        self.assertCountEqual(list(p.skills.values_list('id','name')),upgrade_skill_list)

    """
     On vérifie la mise à jour du compte de xp à partir de différents player reports
    """
    def test_update_Xp(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_Xp()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.total_xp,0)

        # on crée plusieurs rapports de match avec les actions
        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)
        pr = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass = 2,
                                    nb_td = 1,
                                    nb_int = 3,
                                    nb_cas = 1,
                                    mvp = True,)
        pr.update_earned_xps()
        pl1.update_Xp()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.total_xp,18)

        pr = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass = 1,
                                    nb_td = 2,
                                    nb_int = 1,
                                    nb_cas = 2,
                                    mvp = False,)
        pr.update_earned_xps()
        pl1.update_Xp()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.total_xp,31)

    """
     On vérifie les création d'upgrade est bien crée lorsque l'on met à jour les xp
    """
    def test_need_upgrade(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_Xp()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.total_xp,0)

        # on crée plusieurs rapports de match avec les actions
        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)
        pr = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass = 2,
                                    nb_td = 1,
                                    nb_int = 3,
                                    nb_cas = 1,
                                    mvp = False,)
        pr2 = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass =0,
                                    nb_td = 0,
                                    nb_int = 0,
                                    nb_cas = 0,
                                    mvp = True,)
        pr.update_earned_xps()
        pr2.update_earned_xps()
        pl1.update_Xp()
        pl1.update_need_upgrade()

        # on vérifie qu'un upgrade a bien été crée
        self.assertEqual(PlayerUpgrade.objects.filter(player=pl1).count(),2)
        up = PlayerUpgrade.objects.filter(player=pl1).first()

        self.assertEqual(up.value,None)
        self.assertEqual(up.skill,None)
        self.assertEqual(up.status,0)
        self.assertEqual(up.type,1)
        self.assertEqual(up.cost,0)

        # on vérifie que l'orsqu'on delete un rapport d'équipe et que l'on remet à jour les upgrade, le dernier
        # a été supprimé
        pr2.delete()

        pl1.update_Xp()
        pl1.update_need_upgrade()

        self.assertEqual(PlayerUpgrade.objects.filter(player=pl1).count(),1)

        pr2 = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass =0,
                                    nb_td = 0,
                                    nb_int = 0,
                                    nb_cas = 0,
                                    mvp = True,)

        pr2.update_earned_xps()
        pl1.update_Xp()
        pl1.update_need_upgrade()

        # on vérifie qu'un upgrade a bien été crée
        self.assertEqual(PlayerUpgrade.objects.filter(player=pl1).count(),2)


    """
     On vérifie que le joueur est bien supprimé en cas de mort
    """
    def test_player_killed(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)

        # on crée un rapport de mort
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=7,)

        pl1.update_mng()

        # on vérifie que le joueur a bien été supprimé
        self.assertEqual(pl1.id,None)

    """
     On vérifie que le compteur de blessure persistante est bien mis à jour
    """
    def test_niggling_update(self):
         # création du contexte
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                    ref_roster_line = Ref_Roster_Line.objects.get(pk=16))


        # on crée un rapport de match avec une blessure afin de vérifier la maj du compteur de niggling
        mr2 = MatchReportFactory.create()
        tr = TeamReportFacory.create(match=mr2,team=team1)
        PlayerReportFactory.create(player=pl1, team_report=tr, injury_type=2,)

        pl1.update_mng()

        p = Player.objects.get(pk=pl1.id)
        self.assertEqual(p.niggling_injuries,1)


    """
     On vérifie que la sérialization d'un player en mode détail se passe bien
    """
    def test_get_player_detail(self):
        myuser = UserFactory.create()
        team1 = TeamFactory.create(user=myuser,status=1)
        pl1 = PlayerFactory.create(team=team1,
                                   ref_roster_line = Ref_Roster_Line.objects.get(pk=16))

        pl1.update_datas()

        # on crée plusieurs rapports de match avec les actions
        mr2 = MatchReportFactory.create(status=1)
        tr = TeamReportFacory.create(match=mr2,team=team1)
        pr = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass = 2,
                                    nb_td = 1,
                                    nb_int = 3,
                                    nb_cas = 1,
                                    mvp = True,)
        pr2 = PlayerReportFactory.create( player=pl1,
                                    team_report=tr,
                                    nb_pass =1,
                                    nb_td = 1,
                                    nb_int = 1,
                                    nb_cas = 1,
                                    mvp = True,)
        pr.update_earned_xps()
        pr2.update_earned_xps()
        pl1.update_Xp()
        pl1.update_need_upgrade()

        #on va chopper les infos détaillé de ce joueur et voir ce que ça donne
        response = self.client.get("/player/%i/"%pl1.id)

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        player_detail = {
            'id' : 1,
            'name': 'django',
            'num': 2,
            'ref_roster_line': 16,
            'M': 7,
            'F': 3,
            'Ag': 4,
            'Ar': 8,
            'miss_next_game': False,
            'need_upgrade': True,
            'nb_passes': 3,
            'nb_TD': 2,
            'nb_int': 4,
            'nb_cas': 2,
            'nb_MVP': 2,
            'total_xp': 31,
            'is_journeyman': False,
            'skills': {
                0:{'id':3,'name':'Blocage',},
                1:{'id':18,'name':'Glissade contrôlée',},
            }
        }

        self.assertEqual(response.data,player_detail)















