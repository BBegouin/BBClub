__author__ = 'Bertrand'
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from league_manager.views.serializers.skill_serializer import DetailedSkillSerializer
from league_manager.models.ref_skills import Ref_Skills
from django.db.models import Q
from functools import reduce

class SkillList(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DetailedSkillSerializer

    def get_queryset(self):
        """
        this view shall return a skill model list, using catégories
        :return:
        """
        cat_string = self.kwargs['skill_cat']

        queryset = Ref_Skills.objects.filter(reduce(lambda x, y: x | y, [Q(family=cat) for cat in cat_string]))

        return queryset