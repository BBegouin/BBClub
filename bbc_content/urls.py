__author__ = 'Bertrand'

from django.conf.urls import url
from league_manager.views import rest_page

from bbc_content.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_content.views.assets_manager_view import AssetsManagerView

urlpatterns = [

    # blog services
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),

    # upload services
    url(r'^upload/', csrf_exempt(FileUploadView.as_view())),

    # List imgs assets
    url(r'^assets/images', csrf_exempt(AssetsManagerView.as_view())),

    # List vidéos assets



]

urlpatterns = format_suffix_patterns(urlpatterns)
