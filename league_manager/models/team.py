__author__ = 'Bertrand'
from django.db import models
from django.db.models import FileField
from django.contrib.auth.models import User
from mezzanine.utils.models import AdminThumbMixin, upload_to

class Team(models.Model):
    name = models.CharField(max_length=50)
    ref_roster = models.ForeignKey("ref_roster",related_name="roster")
    league = models.ForeignKey("league")
    treasury = models.PositiveSmallIntegerField()
    nb_rerolls = models.PositiveSmallIntegerField()
    pop = models.PositiveSmallIntegerField()
    assistants = models.PositiveSmallIntegerField()
    cheerleaders = models.PositiveSmallIntegerField()
    apo = models.BooleanField()
    coach = models.ForeignKey(User)
    icon_file_path = models.CharField(max_length=500,blank=True,null=True)
    DungeonBowl = models.BooleanField()
    # status value :
    # 0 : draft - base skills needs to be chosen
    # 1 : published : ready to play
    # 2 : level up : need to affect levels up
    # 3 : after match : need to buy some players or retire some others
    status = models.PositiveSmallIntegerField(blank=False,null=False)






