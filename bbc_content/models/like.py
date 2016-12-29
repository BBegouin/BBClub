__author__ = 'Bertrand'
from django.db import models
from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost

class Like(models.Model):
    user = models.ForeignKey(User, verbose_name="Coach")
    post = models.ForeignKey(BlogPost,verbose_name="Post")