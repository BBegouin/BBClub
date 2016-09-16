__author__ = 'Bertrand'
from django.db import models

class Team_Report(models.Model):
    match = models.ForeignKey("match_report")
    team = models.ForeignKey("team")
    score = models.PositiveSmallIntegerField()
    supporters = models.PositiveSmallIntegerField()
    fame = models.PositiveSmallIntegerField()
    winnings = models.PositiveSmallIntegerField()
    fan_factor = models.SmallIntegerField()


