__author__ = 'Bertrand'
from django.db import models
from mezzanine.pages.models import Page

class Author(Page):
    dob = models.DateField("Date of birth")
