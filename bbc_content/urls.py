__author__ = 'Bertrand'

from django.conf.urls import url
from league_manager.views import rest_page

from bbc_content.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_content.views.assets_manager_view import list_image_assets,crop_image,binary_upload

urlpatterns = [

    # blog services
    url(r'^api/post/$', rest_page.post),
    url(r'^api/post/(?P<slug>.+)/$', rest_page.post_content),

    # upload services
    url(r'^upload/$', csrf_exempt(FileUploadView.as_view())),
    url(r'^upload/binary/$', binary_upload),

    # get number of page of corresponding assets type
    #url(r'^assets/images/pages', list_image_assets,name='list_assets'),

    # List imgs assets :
    # optionnal params :
    #    - full : full size images, no need to use size param, may be paginated :
    #       http://localhost:8000/assets/images/?page=1
    #    - thumbs :
    #        - size: medium : medium sized thumbs
    #        - size: small : smal sized thumbs
    #       http://localhost:8000/assets/images/?type=thumbs;size=medium
    #    - cropped :
    #        - size: <number> : cropped of corresponding size
    #
    url(r'^assets/images/$', list_image_assets,name='list_assets'),


    # crop_image
     url(r'^assets/images/crop/$', crop_image,name='crop_image'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
