__author__ = 'Bertrand'

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from collections import OrderedDict
from bbc_auth.tests.datas.facebook_datas import *
from django.contrib.auth.models import User

"""
il faut tester :
- la stabilité des urls
- la stabilités des modèles
"""
class TestLike(APITestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    """
     Test de vérification d'access token facebook :
      - le compte utilisateur n'existe pas,
      - l'identifiant facebook est inconnu dans la base
      - le token d'accès est inconnu
    """
    def test_01_check_unknown_token(self):

        response = self.client.post("/auth/facebook/",wrong_request_data)
        # on vérifie qu'une donnée non-autorisée, ne permet pas de se logguer
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/auth/facebook/",correct_request_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        print(response.data)

    """
     Test de se connexion via facebook :
     - l'identifiant facebook est inconnu,
     - le compte utilisateur existe
     - le token de connexion existe en base
     ==> on vérifie à l'issue de la procédure que le compte utilisateur est lié a l'ID facebook
    """
    def test_01_check_known_user_account(self):
        pass

    """
     Test de se connexion via facebook :
     - l'identifiant facebook est inconnu,
     - le compte utilisateur existe
     - le token de connexion n'existe pas en base
    """
    def test_existing_token(self):
        pass

    """
     Test de se connexion via facebook :
     - l'identifiant facebook est connu,
     - le compte utilisateur existe
     - le token de connexion n'existe pas en base
    """
    def test_existing_token(self):
        pass

    """
     Test de se connexion via facebook :
     - l'identifiant facebook est connu,
     - le compte utilisateur existe
     - le token de connexion existe en base
    """
    def test_existing_token(self):
        pass