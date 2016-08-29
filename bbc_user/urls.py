__author__ = 'Bertrand'

from django.conf.urls import url

from bbc_content.views.fileuploadview import FileUploadView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from bbc_user.views.user_view import UserDetail,UserList, UserDetailFromToken

urlpatterns = [

    # get User List
    url(r'^user/$', UserList.as_view()),

    # Get user detail
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view()),

    #Get user detail from token
    url(r'^user/token/$', UserDetailFromToken.as_view()),

    # Create a user account
]

urlpatterns = format_suffix_patterns(urlpatterns)
