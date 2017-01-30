__author__ = 'Bertrand'
from django.db import models
from league_manager.models.club import Club
from league_manager.models.starting_rules import StartingRules
from django.contrib.auth.models import User

class FacebookUser(models.Model):
    user = models.ForeignKey(User, verbose_name="bbc_user",related_name="facebook_account")
    facebook_id = models.CharField(max_length=255,blank=True,null=True,unique=True)
