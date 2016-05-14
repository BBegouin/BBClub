__author__ = 'Bertrand'
from django.db import models
from mezzanine.pages.models import Page

# le modèle qui va nous permettre de gérer le contenu de notre home page
class Home(Page):
    dob = models.DateField("Date of birth")