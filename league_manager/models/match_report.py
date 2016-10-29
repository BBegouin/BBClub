__author__ = 'Bertrand'
from django.db import models

class MatchReport(models.Model):
    date = models.DateField("Date de la rencontre",null=True)
    # 0: Canicule
    # 1: Très ensoleillé
    # 2: Clément
    # 11: Averse
    # 12: Blizzard
    weather = models.CharField(max_length=50,null=True)
    # status value :
    # 0 : draft : default value
    # 1 : published : impossible to modify
    status = models.PositiveSmallIntegerField(blank=False,null=False)


