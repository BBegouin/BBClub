__author__ = 'Bertrand'
from django.db import models


class Ref_Roster(models.Model):
    name = models.CharField(max_length=30)