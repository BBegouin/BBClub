__author__ = 'Bertrand'
from django.db import models

class Injury_Roll(models.Model):
    dice_value_1 = models.PositiveSmallIntegerField(null=True)
    dice_value_2 = models.PositiveSmallIntegerField(null=True)
    Player_Report = models.ForeignKey("PlayerReport",related_name="injury_roll")
