__author__ = 'Bertrand'


from rest_framework.response import Response
from mezzanine.pages.models import Page
from league_manager.models.general_post import GeneralPost
from league_manager.serializer import GeneralPostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.mail import send_mail

####################################
#
# Allow to :
#   - create an account
#   - check if a useername already exists
#   - retrieve all accounts
#   - retrieve detail of a particular account
#   - delete a particular account
#
####################################



####################################
#
# Create user
#
####################################
"""
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):

    try:
        userName = request.data['username']
        userPass = request.data['password']
        userMail = request.data['email']
    except KeyError:
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: check if already existed
    if userName and userPass and userMail:
        try:
            newUser = User.objects.create_user(username = userName,
                                password = userPass,
                                email = userMail,
                                is_active = False)
            newUser.save()
        except IntegrityError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            send_mail('sujet test',
                      'corps du message',
                      'bloodbowlclub@gmail.com',
                      [userMail],
                      fail_silently=False,)
        except :
            newUser.delete()

        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_204_NO_CONTENT)
"""

####################################
#
# check if user exists
#
####################################
@api_view(['GET'])
@permission_classes((AllowAny,))
def check_username(request,username):

    if username :
       try:
            user = User.objects.get(username=username)
       except ObjectDoesNotExist:
          return Response(status=status.HTTP_200_OK)

       return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
       return Response(status=status.HTTP_204_NO_CONTENT)


    ####################################
#
# check if user exists
#
####################################
@api_view(['GET'])
@permission_classes((AllowAny,))
def check_email(request,email):

    if email :
       try:
            user = User.objects.get(email=email)
       except ObjectDoesNotExist:
          return Response(status=status.HTTP_200_OK)

       return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
       return Response(status=status.HTTP_204_NO_CONTENT)