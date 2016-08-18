from django.test import TestCase

# Create your tests here.
import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import user_username, user_email
from django.core import mail

# liste des catégories de test
#       - tests d'authentification
#       - tests de contenu
class AuthenticationTests(APITestCase):

    auth_token = ""

    # Intialisation des donées de test
    #   - création d'un utilisateur actif
    def setUp(self):
        adapt = get_adapter()
        #create a test user
        usr = adapt.new_user(None)
        usr.set_password('test')
        usr.is_active = 'True'
        user_email(usr, 'bertrand.begouin@gmail.com')
        user_username(usr, 'test')
        usr.save()

        # manually confirm address
        email = EmailAddress.objects.create(user=usr,email='test@test.com')
        adapt.confirm_email(None,email)


    # Teste l'API de connexion, on doit récupérer un token
    def test_login(self):
        url = reverse('rest_login')
        data = {'username': 'test',
                'password': 'test'}

        # on interroge l'api de connexion
        response = self.client.post(url, data, format='json')

        #
        auth_token = response.data['key']
        self.assertIsNotNone(auth_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # on crée un utilisateur,
    # on vérifie la présence en base
    def test_registration(self):
        url = reverse('rest_register')
        data = {'username': 'test2',
                'password1': 'testtest2',
                'password2': 'testtest2',
                'email':'bertrand.begouin@gmail.com',
                'registrationUrl':'http://kikinou.fr/reset/pwd'}

        # on interroge l'api de connexion
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(mail.outbox[0].body)

    # on teste notre mécanisme de reset de mot de mot de passe
    def test_password_reset(self):
        url = reverse('bbc_password_reset')

        data = {'resetUrl': "http://kikinou.fr/reset/pwd",
                'email': 'bertrand.begouin@gmail.com'}

        # on interroge l'api de connexion
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)