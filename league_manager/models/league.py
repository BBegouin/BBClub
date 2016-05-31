__author__ = 'Bertrand'
from django.db import models

class League(models.Model):
    name = models.CharField(max_length=30)

