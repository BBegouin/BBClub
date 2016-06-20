__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views import rest_page
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),
]

urlpatterns = format_suffix_patterns(urlpatterns)
