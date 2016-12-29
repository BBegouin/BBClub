__author__ = 'Bertrand'
from mezzanine.blog.models import BlogPost
from rest_framework import serializers
from bbc_user.views.serializers.user_serializer import UserSerializer
from django_comments.models import Comment
from bbc_content.models.like import Like


class BlogPostDescriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    likes = serializers.SerializerMethodField()

    #on renvoi le nombre de like pour le post
    def get_likes(self, obj):
        return Like.objects.filter(post=obj).count();

    class Meta:
        model = BlogPost
        exclude = ('content','in_sitemap','gen_description','site','short_url','allow_comments')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

class BlogPostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    Comment = CommentSerializer(many=True,read_only=True)
    likes = serializers.SerializerMethodField()

    #on renvoi le nombre de like pour le post
    def get_likes(self, obj):
        return Like.objects.filter(post=obj).count()


    class Meta:
        model = BlogPost

class BlogPostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like


