__author__ = 'Bertrand'
from django.db import models
from league_manager.models.club import Club

class League(models.Model):
    name = models.CharField(max_length=30)
    Club = models.ForeignKey(Club,null=True)

