__author__ = 'Bertrand'
from django.conf.urls import url
from league_manager.views import rest_page
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^page/$', rest_page.page_list),
    url(r'^page/(?P<pk>[0-9]+)/$', rest_page.page_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
