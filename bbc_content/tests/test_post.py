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
class TestPost(APITestCase):

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

        # on crée également les tokens afin que les utilisateurs puissent se loguer
        token = Token.objects.create(user=myuser)
        token.save()
        token = Token.objects.create(user=user2)
        token.save()
        token = Token.objects.create(user=myadmin)
        token.save()

    """

     Test de récupération d'un post

    """
    def test_post_detail(self):
        response = self.client.get(urls["post_list"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.get(urls["post_detail"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    """

     Test de récupération de la liste des post

    """
    def test_post_list(self):
        # on regarde si les codes de statuts correspondent bien à ce que l'on cherche
        # si on fait une requête sans paramètre, on doit avoir tous les status
        response = self.client.get(urls["post_list"])
        post_cpt = BlogPost.objects.count()
        admin_pos_cpt = BlogPost.objects.filter(user__username="admin").count()
        user1_post_cpt = BlogPost.objects.filter(user__username="john_doe").count()
        user2_post_cpt = BlogPost.objects.filter(user__username="user2").count()
        draft_post_cpt = BlogPost.objects.filter(status="1").count()
        published_post_cpt = BlogPost.objects.filter(status="2").count()

        # test de base
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),post_cpt)

        # si on fait une requête avec draft, on doit avoir tous les status 1
        response = self.client.get(urls["post_list_draft"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),draft_post_cpt)

        # si on fait une requête avec published, on doit avoir tous les status 2
        response = self.client.get(urls["post_list_published"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),published_post_cpt)

    """

     Test de création d'un post

    """
    def test_post_create(self):
        #on sauvegarde le nombre d'article avant la création
        Post_num = BlogPost.objects.count()

        # création d'un post interdit pour l'utilisateur anonyme
        response = self.client.post(urls["post_list"],data=create_datas)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.post(urls["post_list"],data=create_datas)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # on vérifie que le post est bien crée
        created_post_id = response.data["id"]
        response = self.client.get(urls["post_list"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),Post_num+1)

        # on vérifie qu'on peut le récupérer
        response = self.client.get("/post/%i/"%created_post_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(created_post_id,response.data["id"] )

    """

     Test de suppression d'un post

    """
    def test_post_delete(self):
        # On sauvegarde le nombre de post avant la suppression
        Post_num = BlogPost.objects.count()

        # on vérifie qu'un utilisateur non identifé n'a pas le droit de faire une suppression
        response = self.client.delete(urls["post_delete"])
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # on vérifie que l'utilisateur connecté a bien le droit de supprimer le post
        # on se connecte avec un utilisateur normal
        self.client.force_authenticate(user=User.objects.get(username="john_doe"))

        # on vérifie qu'on ne peut pas supprimer un post appartenant à un autre utilisateur
        user2_post_id = BlogPost.objects.filter(user__username="admin").first().id
        response = self.client.delete("/post/%d/"%user2_post_id)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # on vérifie qu'on a le droit de supprimer un de ses propres post
        user1_post_id = BlogPost.objects.filter(user__username="john_doe").first().id
        response = self.client.delete("/post/%d/"%user1_post_id)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

        # on vérifie la suppression du post : on vérifie que le comptage des post a diminiué
        response = self.client.get(urls["post_list"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),Post_num-1)

        # On vérifie qu'on arrive pas à attraper le post supprimé
        response = self.client.get("/post/%d/"%user1_post_id)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        # on envoi la requête en tant qu'admin
        self.client.force_authenticate(user=User.objects.get(username="admin"))
        # on vérifie que l'on peut supprimer n'importe quel post
        response = self.client.delete(urls["post_delete"])
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        response = self.client.get(urls["post_delete"])
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response = self.client.get(urls["post_list"])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),Post_num-2)


    def test_post_update(self):
        # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour le post
        user1_post_id = BlogPost.objects.filter(user__username="john_doe").first().id
        admin_post_id = BlogPost.objects.filter(user__username="admin").first().id

        response = self.client.put("/post/%d/"%user1_post_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        #response = self.client.put("/post/%d/"%user1_post_id,)
        response = self.client.put("/post/%d/"%user1_post_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on se connecte avec un utilisateur
        # on vérifie qu'on ne peut pas éditer un post appartenant à un autre utilisateur
        response = self.client.put("/post/%d/"%admin_post_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


    def test_post_partial_update(self):
         # on vérifie que l'utilisateur connecté a bien le droit de mettre a jour le post
        user1_post_id = BlogPost.objects.filter(user__username="john_doe").first().id
        admin_post_id = BlogPost.objects.filter(user__username="admin").first().id

        response = self.client.patch("/post/%d/"%user1_post_id,{"title": "titre mis a jour partiellement"})
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=User.objects.get(username="john_doe"))
        response = self.client.patch("/post/%d/"%user1_post_id,{"title": "titre mis a jour partiellement"})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on vérifie que le pot a bien été mis à jour
        response = self.client.get("/post/%d/"%user1_post_id)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # on se connecte avec un utilisateur
        # on vérifie qu'on ne peut pas éditer un post appartenant à un autre utilisateur
        response = self.client.put("/post/%d/"%admin_post_id,update_datas)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

