__author__ = 'Bertrand'
from django.db import models

class Match_Report(models.Model):
    date = models.DateField("Date de la rencontre")
    weather = models.CharField(max_length=50)


