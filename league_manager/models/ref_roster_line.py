__author__ = 'Bertrand'
from django.db import models
from league_manager.models import ref_roster,ref_skills

class Ref_Roster_Line(models.Model):
    roster = models.ForeignKey("ref_roster",related_name='roster_lines')
    max = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=30)
    cost = models.PositiveSmallIntegerField()
    M = models.PositiveSmallIntegerField()
    F = models.PositiveSmallIntegerField()
    Ag = models.PositiveSmallIntegerField()
    Ar = models.PositiveSmallIntegerField()
    base_skills = models.ManyToManyField("ref_skills")
    normal_skills = models.CharField(max_length=4)
    double_skills = models.CharField(max_length=4)

