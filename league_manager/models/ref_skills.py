__author__ = 'Bertrand'
from django.db import models

class Ref_Skills(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField
    family = models.CharField(max_length=2)


