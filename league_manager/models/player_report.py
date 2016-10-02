__author__ = 'Bertrand'
from django.db import models

class Player_Report(models.Model):
    team_report = models.ForeignKey("team_report")
    player = models.ForeignKey("player")
    nb_pass = models.PositiveSmallIntegerField()
    nb_td = models.PositiveSmallIntegerField()
    nb_int = models.PositiveSmallIntegerField()
    nb_cas = models.PositiveSmallIntegerField()
    nb_mvp = models.PositiveSmallIntegerField()
    nb_foul = models.PositiveSmallIntegerField()
    nb_blocks = models.PositiveSmallIntegerField()
    is_wounded = models.BooleanField()
    serious_casualty = models.PositiveSmallIntegerField()


