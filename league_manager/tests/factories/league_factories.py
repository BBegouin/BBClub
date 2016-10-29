__author__ = 'Bertrand'
import factory

from league_manager.models.league import League
from league_manager.models.club import Club
from league_manager.models.ref_roster import Ref_Roster
from bbc_user.tests.factories.user_factory import UserFactory
from factory.django import DjangoModelFactory

class ClubFactory(DjangoModelFactory):
    class Meta:
        model = Club

    name = "Valdemor Blood Bowl Club"

class LeagueFactory(DjangoModelFactory):
    class Meta:
        model = League

    name = "Ligue de cognac"
    Club = factory.SubFactory(ClubFactory)



