__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.ref_skills import Ref_Skills

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref_Skills
        fields = ('id','name',)

class DetailedSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref_Skills
        fields = ('id','name','family')
