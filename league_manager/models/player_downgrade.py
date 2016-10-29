__author__ = 'Bertrand'
from django.db import models

class PlayerDowngrade(models.Model):
    # 1 : stat decrease M
    # 2 : stat decrease F
    # 3 : stat decrease Ag
    # 4 : stat decrease Ar
    value = models.PositiveSmallIntegerField(null=True)
    player = models.ForeignKey("player",related_name='evolution')
    injury_roll = models.ForeignKey("Injury_Roll",related_name="downgrade")
