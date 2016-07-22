__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views import rest_page
from league_manager.views.rest_views import users
from league_manager.views.rest_views import check_token
from league_manager.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.csrf import csrf_exempt
from league_manager.views.rest_views.lm_password_reset_view import LMPasswordResetView
from league_manager.views.rest_views.facebook_login import FacebookLogin

urlpatterns = [

    # user services
    url(r'^api/user/$', users.create_user),

    # blog services
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),

    # upload services
    url(r'^upload/', csrf_exempt(FileUploadView.as_view())),

    # check_token
    url(r'^api/check-token/', csrf_exempt(check_token.CheckToken)),
    # check_email and user name
    url(r'^api/user/check/email/(?P<email>.+)/$', csrf_exempt(users.check_email)),
    url(r'^api/user/check/(?P<username>.+)/$', users.check_username),

    # password reset
    url(r'^api/password/reset/$', csrf_exempt(LMPasswordResetView.as_view())),

    #
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')

]

urlpatterns = format_suffix_patterns(urlpatterns)
