__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views import rest_page
from league_manager.views.rest_views import users
from league_manager.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # user services
    url(r'^api/user/check/(?P<username>.+)/$', users.check_username),
    url(r'^api/user/$', users.create_user),

    # blog services
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),

    # upload services
    url(r'^upload/', csrf_exempt(FileUploadView.as_view())),
]

urlpatterns = format_suffix_patterns(urlpatterns)
