__author__ = 'Bertrand'
from django.db import models

class Xp_Roll(models.Model):
    dice_value_1 = models.PositiveSmallIntegerField(null=True)
    dice_value_2 = models.PositiveSmallIntegerField(null=True)
    Player_Report = models.ForeignKey("PlayerReport",related_name="xp_roll")
