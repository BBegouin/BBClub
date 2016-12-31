__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from mezzanine.blog.models import BlogPost
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from bbc_content.tests.factories.post_factories import BlogPostFactory
from django_comments.models import Comment
from bbc_content.tests.datas.urls import *
from bbc_content.tests.datas.post_datas import *
from django.contrib.auth.models import User

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestComment(APITestCase):

    @classmethod
    def setUpTestData(cls):
        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        myadmin = AdminFactory.create()
        BlogPostFactory.create_batch(size=2,user=myuser,status=2)
        BlogPostFactory.create_batch(size=2,user=myadmin,status=2)

    """

     Test de création d'un commentaire de post

    """
    def test_a_create_comment(self):
        post = BlogPost.objects.all().first()
        user2 = User.objects.get(username="user2")
        comment_data = {"object_pk":post.id,
                   "user":user2.id,
                   "user_name":user2.username,
                   "comment":"salut les <strong>connasses</strong> !!!! ",
                   "submit_date":"2016-09-23T15:49:05Z",
                   "content_type":32,
                    "site":1,
                   }

        response = self.client.post("/comment/",comment_data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        #on vérifie qu'après avoir connecté le bon utilisateur le dé-like fonctionne
        self.client.force_authenticate(user=User.objects.get(username="user2"))
        response = self.client.post("/comment/",comment_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        #on vérifie que l'on peut attraper le commentaire en BDD
        self.assertEqual(Comment.objects.filter(object_pk=post.id).count(),1)

        comment = Comment.objects.get(object_pk=post.id)


