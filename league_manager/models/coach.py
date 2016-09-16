__author__ = 'Bertrand'
from django.db import models
from league_manager.models.club import Club


class Coach(models.Model):
    photo = models.ImageField(upload_to="coachs")
    Club = models.ForeignKey(Club,null=True)
