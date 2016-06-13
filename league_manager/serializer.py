from rest_framework import serializers
from django.db import models
from league_manager.models.pages.general_page import GeneralPage

from mezzanine.pages.models import Page

class PageSerializer(serializers.ModelSerializer):
    parent = models.ForeignKey(Page, related_name='parent')
    class Meta:
        model = Page
        fields = ('id','title','slug',  'content_model','description','in_menus','parent')

