__author__ = 'Bertrand'
import factory

from league_manager.models.team import Team
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.league import League
from bbc_user.tests.factories.user_factory import UserFactory
from datetime import datetime,timedelta
from league_manager.tests.factories.league_factories import LeagueFactory
from factory.django import DjangoModelFactory

class FakeTeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    name = "les boeufs crevés"
    ref_roster = Ref_Roster.objects.get(name="Elfes Pros")
    league = League.objects.first()
    treasury = 10
    nb_rerolls = 2
    pop = 3
    assistants = 0
    cheerleaders = 0
    apo = False
    user = factory.SubFactory(UserFactory)
    icon_file_path = "icon file path"
    DungeonBowl = False
    # status value :
    # 0 : draft - base skills needs to be chosen
    # 1 : published : ready to play
    # 2 : level up : need to affect levels up
    # 3 : after match : need to buy some players or retire some others
    status = 1


