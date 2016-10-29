__author__ = 'Bertrand'
import factory

from league_manager.models.player import Player
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.league import League
from bbc_user.tests.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory

class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    name = "django"
    miss_next_game = False
    ref_roster_line = Ref_Roster_Line.objects.get(pk=45)
    num = 2
    total_xp = 4
    need_upgrade = False


