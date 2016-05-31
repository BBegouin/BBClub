__author__ = 'Bertrand'
from django.db import models
from league_manager.models.club import Club


class Coach(models.Model):
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField
    photo = models.ImageField(upload_to="coachs")
    Club = models.ForeignKey(Club,null=True)
