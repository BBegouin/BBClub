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
class TestUsers(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    """
     On vérifie l'application les upgrade lorsque l'on applique les upgrades
    """
    def test_get_user_list(self):
        myuser = UserFactory.create()
        myuser2 = UserFactory.create(username="user2")

        self.client.force_authenticate(user=myuser)

        # on lance la création d'une équipe
        response = self.client.get("/user/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)













