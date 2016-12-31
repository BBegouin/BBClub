__author__ = 'Bertrand'
from mezzanine.blog.models import BlogPost
from rest_framework import serializers
from bbc_user.views.serializers.user_serializer import UserSerializer
from mezzanine.generic.models import ThreadedComment
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

class CommentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThreadedComment
        exclude = ('user_url','user_email','ip_address','is_public','is_removed','rating_count','rating_sum','rating_average','by_author','content_type','site','user')

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThreadedComment
        exclude = ('user_url','user_email','ip_address','is_public','is_removed','rating_count','rating_sum','rating_average','by_author')

class BlogPostDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
    comments = CommentListSerializer(many=True,read_only=True)
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


