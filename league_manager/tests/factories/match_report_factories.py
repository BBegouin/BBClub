__author__ = 'Bertrand'
import factory

from league_manager.models.match_report import MatchReport
from league_manager.models.team_report import TeamReport
from league_manager.models.player_report import PlayerReport
from league_manager.tests.factories.team_factories import TeamFactory

from factory.django import DjangoModelFactory
from datetime import datetime,timedelta

class PlayerReportFactory(DjangoModelFactory):
    class Meta:
        model = PlayerReport

    nb_pass = 1
    nb_td = 1
    nb_int = 1
    nb_cas = 1
    nb_mvp = 1
    nb_foul = 1
    nb_blocks = 21
    is_wounded = False

class TeamReportFacory(DjangoModelFactory):
    class Meta:
        model = TeamReport

    team = factory.SubFactory(TeamFactory)
    supporters = 12
    fame = 1
    winnings = 50
    fan_factor = -1
    other_casualties = 1


class MatchReportFactory(DjangoModelFactory):
    class Meta:
        model = MatchReport

    date = factory.LazyFunction(datetime.now)
    weather = 2
    status = 0






