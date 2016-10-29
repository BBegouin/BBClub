__author__ = 'Bertrand'
from django.db import models
from league_manager.models.club import Club
from league_manager.models.starting_rules import StartingRules

class League(models.Model):
    name = models.CharField(max_length=30)
    Club = models.ForeignKey(Club,null=True)
    starting_rules = models.ForeignKey(StartingRules,null=True)

