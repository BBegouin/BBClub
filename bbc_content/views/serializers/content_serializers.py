__author__ = 'Bertrand'
from mezzanine.blog.models import BlogPost
from rest_framework import serializers
from bbc_user.views.serializers.user_serializer import UserSerializer
from django_comments.models import Comment

class BlogPostDescriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True);

    class Meta:
        model = BlogPost
        exclude = ('content','in_sitemap','gen_description','site','short_url','allow_comments')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

class BlogPostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True);
    Comment = CommentSerializer(many=True,read_only=True);

    class Meta:
        model = BlogPost

class BlogPostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost


