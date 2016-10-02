__author__ = 'Bertrand'
from django.db import models

class PlayerEvolution(models.Model):
    # 0 : simple skill
    # 1 : double skill
    # 2 : stat increase M
    # 3 : stat increase F
    # 4 : stat increase Ag
    # 5 : stat increase Ar
    # 6 : stat decrease M
    # 7 : stat decrease F
    # 8 : stat decrease Ag
    # 9 : stat decrease Ar
    value = models.PositiveSmallIntegerField(null=True)
    player_id = models.ForeignKey("player")
    new_skill = models.ManyToManyField("ref_skills", blank=True, null=True)
    # 0 : to be done
    # 1 : done
    status = models.PositiveSmallIntegerField(null=True)
    # 0 : additionnal base skills
    # 1 : Xp
    type = models.PositiveSmallIntegerField()
