__author__ = 'Bertrand'

from django.conf.urls import url

from bbc_content.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_content.views.assets_manager_view import list_image_assets,crop_image,binary_upload
from bbc_content.views.post_view import PostList,PostDetail,PostCreate

urlpatterns = [

    # blog services

    # List all the blogs post
    url(r'^post/$', PostList.as_view()),

    # Create or update a post
    url(r'^post/create/$', PostCreate.as_view()),

    # Get a post detail
    url(r'^post/(?P<pk>.+)/$', PostDetail.as_view()),


    # upload services : upload a file
    url(r'^upload/$', csrf_exempt(FileUploadView.as_view())),

    # upload services : upload a binary string from an html img.src tag
    url(r'^upload/binary/$', binary_upload),

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
