__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase
from mezzanine.blog.models import BlogPost
from bbc_user.tests.factories.user_factory import UserFactory,AdminFactory
from bbc_content.tests.factories.post_factories import BlogPostFactory
from rest_framework.authtoken.models import Token
from bbc_content.tests.datas.urls import *
from bbc_content.tests.datas.post_datas import *
from django.contrib.auth.models import User

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestAssets(APITestCase):

    @classmethod
    def setUpTestData(cls):
        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        myadmin = AdminFactory.create()

        # on crée également les tokens afin que les utilisateurs puissent se loguer
        Token.objects.create(user=myuser).save()
        Token.objects.create(user=user2).save()
        Token.objects.create(user=myadmin).save()