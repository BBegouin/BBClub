__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views import rest_page
from league_manager.views.rest_views import users
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # user services
    # cette création utilisateur semble complètement merdique !!! url(r'^api/user/$', users.create_user),

    # blog services
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),

    # check_email and user name
    url(r'^api/user/check/email/(?P<email>.+)/$', csrf_exempt(users.check_email)),
    url(r'^api/user/check/(?P<username>.+)/$', users.check_username),
]

urlpatterns = format_suffix_patterns(urlpatterns)
