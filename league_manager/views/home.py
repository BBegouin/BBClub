__author__ = 'Bertrand'
from django.shortcuts import render
from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost

def tous_les_utilisateurs(request):
    context = {"posts": BlogPost.objects.all()}
    return render(request, "index.html", context)
