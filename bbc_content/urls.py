__author__ = 'Bertrand'

from django.conf.urls import url

from bbc_content.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_content.views.assets_manager_view import list_image_assets,crop_image,binary_upload
from bbc_content.views import post_view_set
from bbc_content.views import like_view_set
from rest_framework import routers
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'post', post_view_set.PostViewSet)
router.register(r'like', like_view_set.LikeViewSet)

urlpatterns = [
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
urlpatterns += router.urls


