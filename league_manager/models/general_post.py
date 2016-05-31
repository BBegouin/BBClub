__author__ = 'Bertrand'
from django.db import models
from mezzanine.blog.models import BlogPost

# le modèle qui va nous permettre de gérer le contenu de notre home page
class GeneralPost(BlogPost):
    sub_title = models.CharField(max_length=150)