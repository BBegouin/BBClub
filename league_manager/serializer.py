from rest_framework import serializers
from django.db import models
from league_manager.models.general_post import GeneralPost
from league_manager.models.pages.general_page import GeneralPage

from mezzanine.pages.models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralPage

class GeneralPostSerializer(serializers.ModelSerializer):
    class Meta :
        model = GeneralPost

