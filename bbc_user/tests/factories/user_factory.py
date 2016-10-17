__author__ = 'Bertrand'

import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = 'John'
    last_name = 'Doe'
    email= 'john@doe.com'
    password= 'pwdtest'
    username= 'john_doe'
    is_superuser = False

class AdminFactory(DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = 'TestAdmin_firstname'
    last_name = 'TestAdmin_lastname'
    email= 'admin@gmail.com'
    password= 'adminpwdtest'
    username= 'admin'
    is_superuser = True
