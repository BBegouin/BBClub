__author__ = 'Bertrand'
import factory

from league_manager.models.player_upgrade import PlayerUpgrade
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.league import League
from bbc_user.tests.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory

class PlayerUpgradeFactory(DjangoModelFactory):
    class Meta:
        model = PlayerUpgrade

    # 0 : simple skill
    # 1 : double skill
    # 2 : stat increase M
    # 3 : stat increase F
    # 4 : stat increase Ag
    # 5 : stat increase Ar
    value = None
    # 0 : to be done
    # 1 : done
    status = 0
    # 0 : additionnal base skills
    # 1 : Xp
    type = 1



