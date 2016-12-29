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
from bbc_content.models.like import Like
from collections import OrderedDict
"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestLike(APITestCase):

    @classmethod
    def setUpTestData(cls):
        myuser = UserFactory.create()
        user2 = UserFactory.create(username="user2",password="user2")
        myadmin = AdminFactory.create()
        BlogPostFactory.create_batch(size=2,user=myuser,status=1)
        BlogPostFactory.create_batch(size=2,user=myadmin,status=1)
        BlogPostFactory.create_batch(size=3,user=myuser,status=2)
        BlogPostFactory.create_batch(size=2,user=myadmin,status=2)
        BlogPostFactory.create_batch(size=2,user=user2,status=2)


    """

     Test de like d'un post

    """
    def test_like_post(self):

        # récupération d'un post
        post_id = BlogPost.objects.all().first().id
        # récupération d'un id de user
        user_id = User.objects.all().first().id

        # on vérifie que l'on peut liker un post
        # on vérifie que l'on ne peut pas liker un post draft
        like_post_data = {
            "user": user_id,
            "post": post_id,
        }

        like_count = Like.objects.all().count()
        response = self.client.post("/like/",like_post_data)
        #on vérifie qu'on ne peut pas liker lorsque non loggé
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="user2"))
        response = self.client.post("/like/",like_post_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        self.assertEqual(Like.objects.all().count(),like_count+1)
        lik = Like.objects.all().last()
        self.assertEqual(lik.user.id,user_id)
        self.assertEqual(lik.post.id,post_id)

        #on vérifie la récupération de la liste des posts
        response = self.client.get("/like/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    """
     Test de récupération de likes, tous, par user, et par post
    """
    def a_test_get_like(self):

        # On crée des like :
        # user_1 va liker 3 posts
        # user_2 va liker 2 posts
        like_count = Like.objects.all().count()
        user_1 = User.objects.get(username="user2")
        user_2 = User.objects.get(username="admin")
        post_1 = BlogPost.objects.filter(user__username ="john_doe",status = 2).first()
        post_2 = BlogPost.objects.filter(user__username ="admin",status = 2).first()
        post_3 = BlogPost.objects.filter(user__username ="user2",status = 2).first()

        like_post_data = [{ "user": user_1, "post": post_1},
                          { "user": user_1, "post": post_2},
                          { "user": user_2, "post": post_2},
                          { "user": user_2, "post": post_3},
                          { "user": user_2, "post": post_1}]

        for like_data in like_post_data:
            lik = Like(user = like_data["user"],post=like_data["post"])
            lik.save()

        self.assertEqual(Like.objects.all().count(),like_count+5)

        # on essaye de récupérer tous les like, on doit en avoir 5
        response = self.client.get("/like/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #on vérifie le retour de l'API
        ref_data = [ OrderedDict([('id',1),('user',user_1.id),('post',post_1.id)]),
                     OrderedDict([('id',2),('user',user_1.id),('post',post_2.id)]),
                     OrderedDict([('id',3),('user',user_2.id),('post',post_2.id)]),
                     OrderedDict([('id',4),('user',user_2.id),('post',post_3.id)]),
                     OrderedDict([('id',5),('user',user_2.id),('post',post_1.id)]) ]

        self.assertEqual(ref_data,response.data)
        # on essaye de récupérer les like de user_1 on doit en avoir 2
        response = self.client.get("/like/?user_id=%i"%user_1.id)
        self.assertEqual(ref_data[:2],response.data)
        # on essaye de récupérer les like de user_2 on doit en avoir 3
        response = self.client.get("/like/?user_id=%i"%user_2.id)
        self.assertEqual(ref_data[-3:],response.data)
        # on essaye de récupérer les like sur le post 3 on doit en avoir 1
        response = self.client.get("/like/?post_id=%i"%post_3.id)
        self.assertEqual(ref_data[3:4],response.data)
        # on essaye de récupérer les like sur le post 1 on doit en avoir 2
        response = self.client.get("/like/?post_id=%i"%post_2.id)
        self.assertEqual(ref_data[1:3],response.data)
        # on essaye de récupérer les like sur le post 1 par l'utilisateur user_1, on doit en avoir 1
        response = self.client.get("/like/?post_id=%i&user_id=%i"%(post_2.id,user_1.id))
        self.assertEqual(ref_data[:1],response.data)

        #on vérifie qu'en récupérant les infos du post post_2, le nombre de like est bien de 2
        response = self.client.get("/post/%i/"%post_2.id)
        self.assertEqual(2,response.data["likes"])
        response = self.client.get("/post/%i/"%post_3.id)
        self.assertEqual(1,response.data["likes"])

    """
     Test de suppression de likes, en utilisant user et post
    """
    def b_test_delete_like(self):

        #initialisation -------------------------------

        like_count = Like.objects.all().count()
        user_1 = User.objects.get(username="user2")
        post_1 = BlogPost.objects.filter(user__username ="john_doe",status = 2).first()


        like_post_data = [{ "user": user_1, "post": post_1}]

        lik_id = 0
        for like_data in like_post_data:
            lik = Like(user = like_data["user"],post=like_data["post"])
            lik.save()
            lik_id = lik.id

        self.assertEqual(Like.objects.all().count(),like_count+1)

        # test ----------------------------------------

        #on vérifie que seul le propriétaire d'un like peut dé-liker
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        response = self.client.delete("/like/dislike/?post_id=%i&user_id=%i"%(post_1.id,user_1.id))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        #on vérifie qu'après avoir connecté le bon utilisateur le dé-like fonctionne
        self.client.force_authenticate(user=User.objects.get(username="user2"))
        #response = self.client.delete("/like/%i/"%lik_id)
        response = self.client.delete("/like/dislike/?post_id=%i&user_id=%i"%(post_1.id,user_1.id))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        #on vérifie que le like n'existe plus
        self.assertEqual(Like.objects.all().count(),like_count)