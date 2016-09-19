__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.ref_roster import Ref_Roster
from league_manager.models.ref_roster_line import Ref_Roster_Line
from league_manager.models.ref_skills import Ref_Skills

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ref_Skills
        fields = ('id','name',)

class RosterLineSerializer(serializers.ModelSerializer):
    base_skills = SkillSerializer(many=True,read_only=True);

    class Meta:
        model = Ref_Roster_Line
        fields = ('id','max','position','cost','M','F','Ag','Ar','base_skills','normal_skills','double_skills')

class RosterListSerializer(serializers.ModelSerializer):
    roster_lines = RosterLineSerializer(many=True,read_only=True);

    class Meta:
        model = Ref_Roster
        fields = ('id','name','reroll_price','apo_available','roster_lines')

