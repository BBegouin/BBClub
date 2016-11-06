__author__ = 'Bertrand'
from django.db import models
import django


class RankingRules(models.Model):
    win_point = django.db.models.SmallIntegerField()
    draw_point = django.db.models.SmallIntegerField()
    lose_point = django.db.models.SmallIntegerField()

