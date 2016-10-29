__author__ = 'Bertrand'
from django.db import models

class PlayerReport(models.Model):
    team_report = models.ForeignKey("TeamReport",related_name="player_report")
    player = models.ForeignKey("player")
    nb_pass = models.PositiveSmallIntegerField(default=0)
    nb_td = models.PositiveSmallIntegerField(default=0)
    nb_int = models.PositiveSmallIntegerField(default=0)
    nb_cas = models.PositiveSmallIntegerField(default=0)
    nb_mvp = models.PositiveSmallIntegerField(default=0)
    nb_foul = models.PositiveSmallIntegerField(default=0)
    nb_blocks = models.PositiveSmallIntegerField(default=0)
    is_wounded = models.BooleanField(default=False)
    # 0 Commotion Aucun effet à long terme
    # 1 un match d'arrêt
    # 2 blessure persistante
    # 3 -1 M
    # 4 -1 Ar
    # 5 -1 Ag
    # 6 -1 F
    # 7 Mort
    injury_type = models.PositiveSmallIntegerField(null=True)
    earned_xp = models.PositiveSmallIntegerField(null=True)
