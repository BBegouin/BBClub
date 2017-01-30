__author__ = 'Bertrand'
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
import facebook
from facebook import GraphAPIError
from bbc_user.models.facebook_user import FacebookUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
#from bbc_auth.views.adapters import facebook_adapter
#from bbc_auth.tests.adapters import facebook_adapter
import importlib



"""
 Méthode à utiliser pour se connecter grâce à son compte facebook.
 - si le compte utilisateur BBC n'existe pas, on le crée
 - si le compte existe, on voit si on peut le lier a l'id facebook
"""
@api_view(['POST'])
@permission_classes((AllowAny,))
def FacebookLogin(request):

    facebook_id  = request.data['userID']
    access_token = request.data['accessToken']

    #on instancie l'adaptateur qui va bien
    module = importlib.import_module(settings.FACEBOOK_ADAPTER)
    facebook_adapter = module.getAdapter()

    # création de l'objet graph, à partir du token d'accès reçu
    graph = facebook_adapter.GraphAPI(access_token=access_token)

    try:
         graph.get_object("me")
    except GraphAPIError:
        return Response("accès invalide",status=status.HTTP_401_UNAUTHORIZED)

    # si on arrive dans cette partie le token d'accès est valide pour l'utilisateur.
    fb_user = graph.get_object("me",fields='first_name,last_name,email,picture')

    # on regarde si l'id facebook à déjà été associé à un compte utilisateur
    user = None
    try:
        user = FacebookUser.objects.get(facebook_id=facebook_id).user
    except ObjectDoesNotExist:
        # si on ne trouve pas l'objet, facebook Id,
        # on regarde, est-ce qu'on aurait déjà un compte utilisateur, non lié à facebook, dont l'email correspond
        try :
            user = User.objects.get(email=fb_user['email'])
        except ObjectDoesNotExist:
            # si on n'a pas trouvé de compte utilisateur, alors on le crée
            user = createUserAccountFromFacebook(fb_user,facebook_id)
        except MultipleObjectsReturned:
            #on a plusieurs comptes utilisateurs avec la même adresse mail, ce qui ne devrait pas arriver
                return Response("plusieurs comptes avec la même adresse email",status=status.HTTP_406_NOT_ACCEPTABLE)

        # on lie le compte utilisateur à l'id facebook
        link_fb_account_and_user_account(user,facebook_id)

    # - on logue l'utilisateur dont l'id est lié à l'id facebook
    # est-ce qu'on a un token pour l'utilisateur ?
    try :
        token = Token.objects.get(user=user)
    except ObjectDoesNotExist:
        token = Token.objects.create(user=user)

    return Response("%s"%token,status=status.HTTP_200_OK)


"""
 Méthode à utiliser pour créer un compte, grâce à son compte facebook :
 - on crée un compte utilisateur à partir des données de facebook
"""
@api_view(['POST'])
@permission_classes((AllowAny,))
def FacebookCreateAccount(request):
    pass

@api_view(['POST'])
@permission_classes((AllowAny,))
def FacebookLinkAccount(request):
    pass

#
# Crée un utilisateur BBC à partir des infos facebook
#
def createUserAccountFromFacebook(fb_user, facebook_id):

    # création du compte utilisateur
    new_user = User(is_superuser=False,
                    is_staff = False,
                    is_active = True,
                    first_name=fb_user['first_name'],
                    last_name=fb_user['last_name'],
                    username=fb_user['email'],
                    email=fb_user['email'])
    new_user.save()

    #TBD :  #il faut également que l'email soit considéré comme vérifié
    return new_user

def link_fb_account_and_user_account(user,fb_id):
    #association du compte utilisateur et du compte facebook
    FB_user = FacebookUser(user=user,facebook_id=fb_id)
    FB_user.save()

