__author__ = 'Bertrand'
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.views.serializers.skill_serializer import SkillSerializer
from rest_framework import serializers

class RosterLineSerializer(serializers.ModelSerializer):
    base_skills = SkillSerializer(many=True,read_only=True)

    class Meta:
        model = Ref_Roster_Line
        fields = ('id','max','position','cost','M','F','Ag','Ar','base_skills','normal_skills','double_skills')
