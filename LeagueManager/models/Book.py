__author__ = 'Bertrand'
from django.db import models
from mezzanine.pages.models import Page

class Book(models.Model):
    author = models.ForeignKey("Author")
    cover = models.ImageField(upload_to="authors")


