__author__ = 'Bertrand'
from django.db import models
from mezzanine.pages.models import Page

# le modèle qui va nous permettre de gérer le contenu de la page des coachs
class GeneralPage(Page):
    ICON_CHOICES = (
        ('torso','torso',),
        ('torsos-all','torsos-all',),
        ('home','home'),
    )
    menuIcon = models.CharField(max_length=50,
                                choices=ICON_CHOICES,
                                default='torso')