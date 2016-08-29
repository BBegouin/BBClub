__author__ = 'Bertrand'

from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
#    blogposts = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name','last_name')