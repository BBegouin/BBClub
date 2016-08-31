__author__ = 'Bertrand'
from mezzanine.blog.models import BlogPost
from rest_framework import serializers
from bbc_user.views.serializers.user_serializer import UserSerializer

class BlogPostDescriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True);
    
    class Meta:
        model = BlogPost
        exclude = ('content','in_sitemap','gen_description','site','short_url','allow_comments')

class BlogPostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True);

    class Meta:
        model = BlogPost