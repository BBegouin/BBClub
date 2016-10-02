__author__ = 'Bertrand'
from rest_framework import serializers
from league_manager.models.ref_roster import Ref_Roster
from league_manager.views.serializers.roster_line_serializer import RosterLineSerializer


class RosterListSerializer(serializers.ModelSerializer):
    roster_lines = RosterLineSerializer(many=True,read_only=True);

    class Meta:
        model = Ref_Roster
        fields = ('id','name','reroll_price','apo_available','roster_lines')

