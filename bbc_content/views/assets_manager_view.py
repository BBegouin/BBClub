__author__ = 'Bertrand'

import re
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings

import math

@method_decorator(csrf_exempt, name='get')
class AssetsManagerView(APIView):

    permission_classes = (AllowAny,)

    # list all assets
    def get(self, request):

        type = None
        size = None
        page = None

        if self.request.query_params.get('type', None):
            type = self.request.query_params.get('type', None)

        if self.request.query_params.get('size', None):
            size = self.request.query_params.get('size', None)

        if self.request.query_params.get('page', None):
            page = int(self.request.query_params.get('page', None))

        path = getattr(settings, "MEDIA_ROOT", None)+"/uploads/";
        if type is not None:
            if type == "thumbs" :
                path +=  "thumbnails/medium"

                if size == "small":
                   path +=  "thumbnails/small"

            elif type == "cropped":
               path +=  "cropped/"+size

        img_list =os.listdir(path)
        img_list = [file for file in img_list if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif"))]

        # manage pagination
        if page is not None:
            pagemax = math.ceil(len(img_list)/10)
            if page > pagemax:
                page = pagemax

            if page < 1:
                page = 1

            startIndex = (page - 1)*10;

            stopindex = 0
            if len(img_list) < page*10:
                stopindex = len(img_list)
            else:
                stopindex = page*10

            img_list = img_list[startIndex:stopindex]

        return Response(img_list, status.HTTP_200_OK)

