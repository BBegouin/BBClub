__author__ = 'Bertrand'
from mezzanine.blog.models import BlogPost
from rest_framework import serializers

class BlogPostDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        exclude = ('content','in_sitemap','gen_description','site','short_url','allow_comments')

class BlogPostDetailSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = BlogPost