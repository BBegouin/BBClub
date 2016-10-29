__author__ = 'Bertrand'
from django.db import models
import django


class StartingRules(models.Model):
    max_budget = django.db.models.SmallIntegerField()
    max_simple_skills = django.db.models.SmallIntegerField()
    max_double_skills = django.db.models.SmallIntegerField()

