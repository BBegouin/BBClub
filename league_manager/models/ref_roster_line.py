__author__ = 'Bertrand'
from django.db import models
from league_manager.models import ref_roster,ref_skills

class Ref_Roster_Line(models.Model):
    max = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=30)
    cost = models.PositiveSmallIntegerField()
    M = models.PositiveSmallIntegerField()
    Ag = models.PositiveSmallIntegerField()
    F = models.PositiveSmallIntegerField()
    Ar = models.PositiveSmallIntegerField()
    roster = models.ForeignKey("ref_roster")
    #compétences
    skills = models.ManyToManyField("ref_skills")

