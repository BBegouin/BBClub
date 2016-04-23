__author__ = 'Bertrand'
from django.db import models

class Match(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField("Date de la rencontre")


