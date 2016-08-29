__author__ = 'Bertrand'

from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_auth.views.bbc_password_reset_view import BBCPasswordResetView
from bbc_auth.views import check_token
from bbc_auth.views.facebook_login import FacebookLogin

#
# Remote Auth App is meant to wrap django allauth, rest_auth, and to customize the mechanism
# of subscribtion, lost login etc.
#
#
urlpatterns = [

    # check auth token _token
    #TODO : remove the function to use the built-in user function
    url(r'^auth/check-token/', csrf_exempt(check_token.CheckToken)),

    # Endpoint to connect using facebook Oauth
    #TODO : implement facebook login - postponed due to deployment
    url(r'^auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    # password reset : customisation for sending html emails
    #TODO implement a child of the register view and lost login view, in order to don't let the back end depend on the backend
    url(r'^auth/password/reset/$', BBCPasswordResetView.as_view(),name='bbc_password_reset'),

    # include unmodified code from rest_auth and allauth
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),

    url(r'^allauth/', include('allauth.urls')),
    url(r'^allauth/account/', include('allauth.account.urls')),



    #TODO : implement a service to send on demand the email for account confirmation

]

urlpatterns = format_suffix_patterns(urlpatterns)
