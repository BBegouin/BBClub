__author__ = 'Bertrand'
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)
    ref_roster_line = models.ForeignKey("ref_roster_line")
    skills = models.ManyToManyField("ref_skills")
    team = models.ForeignKey("team")
    xp = models.PositiveSmallIntegerField
    miss_next_game = models.BooleanField
    persistant_injuries = models.PositiveSmallIntegerField
    nb_pass = models.PositiveSmallIntegerField
    nb_td = models.PositiveSmallIntegerField
    nb_int = models.PositiveSmallIntegerField
    nb_sor = models.PositiveSmallIntegerField
    nb_aggro = models.PositiveSmallIntegerField
    nb_jpv = models.PositiveSmallIntegerField