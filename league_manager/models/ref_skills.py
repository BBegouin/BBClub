__author__ = 'Bertrand'
from django.db import models
import django


class Ref_Skills(models.Model):
    name = django.db.models.CharField(max_length=30)
    desc = django.db.models.TextField()
    family = django.db.models.CharField(max_length=2)
