__author__ = 'Bertrand'
from django.db import models

class Ref_Roster(models.Model):
    name = models.CharField(max_length=30)
    reroll_price = models.PositiveIntegerField()
    apo_available = models.BooleanField()
    journeyman = models.ForeignKey("Ref_Roster_Line",null=True)
