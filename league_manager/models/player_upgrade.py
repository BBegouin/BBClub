__author__ = 'Bertrand'
from django.db import models

class PlayerUpgrade(models.Model):
    # 0 : simple skill
    # 1 : double skill
    # 2 : stat increase M
    # 3 : stat increase F
    # 4 : stat increase Ag
    # 5 : stat increase Ar
    value = models.PositiveSmallIntegerField(null=True)
    player = models.ForeignKey("player",related_name='upgrade')
    skill = models.ForeignKey("ref_skills", blank=True, null=True)
    # 0 : to be done
    # 1 : done
    status = models.PositiveSmallIntegerField(null=True)
    # 0 : additionnal base skills
    # 1 : Xp
    type = models.PositiveSmallIntegerField()
    xp_roll = models.ForeignKey("Xp_Roll",related_name="upgrade")
