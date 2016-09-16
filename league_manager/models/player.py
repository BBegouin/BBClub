__author__ = 'Bertrand'
from django.db import models
import django

class Player(models.Model):
    name = django.db.models.CharField(max_length=50)
    miss_next_game = django.db.models.BooleanField()
    ref_roster_line = django.db.models.ForeignKey("ref_roster_line")
    team = django.db.models.ForeignKey("team")
