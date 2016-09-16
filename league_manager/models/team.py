__author__ = 'Bertrand'
from django.db import models
from django.db.models import ImageField
from mezzanine.utils.models import AdminThumbMixin, upload_to

class Team(models.Model):
    name = models.CharField(max_length=50)
    ref_roster = models.ForeignKey("ref_roster")
    league = models.ForeignKey("league")
    treasury = models.PositiveSmallIntegerField()
    nb_rerolls = models.PositiveSmallIntegerField()
    pop = models.PositiveSmallIntegerField()
    assistants = models.PositiveSmallIntegerField()
    cheerleeders = models.PositiveSmallIntegerField()
    apo = models.BooleanField()
    igor = models.BooleanField()
    cuistot = models.BooleanField()
    coach = models.ForeignKey("coach")
    icon_file = ImageField(upload_to=("team_icons"))
    DungeonBowl = models.BooleanField()






