__author__ = 'Bertrand'
from django.db import models

class TeamReport(models.Model):
    match = models.ForeignKey("MatchReport",related_name="team_reports")
    team = models.ForeignKey("team", related_name="report")
    supporters = models.PositiveSmallIntegerField(null=True)
    fame = models.PositiveSmallIntegerField(null=True)
    winnings = models.PositiveSmallIntegerField(null=True)
    fan_factor = models.SmallIntegerField(null=True)
    other_casualties = models.SmallIntegerField(null=True)


