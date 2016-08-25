__author__ = 'Bertrand'

import re
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings

from django.core.files.storage import FileSystemStorage

@method_decorator(csrf_exempt, name='get')
class AssetsManagerView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format='jpg'):
        path = getattr(settings, "MEDIA_ROOT", None)+"/uploads/thumbnails/medium"
        img_list =os.listdir(path)
        img_list = [file for file in img_list if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif"))]
        return Response(img_list, status.HTTP_200_OK)

