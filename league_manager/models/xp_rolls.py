__author__ = 'Bertrand'
from django.db import models

class Xp_Roll(models.Model):
    name = models.CharField(max_length=30)
    Values = models.CharField(max_length=30)
    player_id = models.ForeignKey("player")
