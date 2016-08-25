__author__ = 'Bertrand'


import os
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.conf import settings

import math

PAGE_SIZE = 10

 # list all assets
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_image_assets(request):

    type = None
    size = None
    page = None

    if request.query_params.get('type', None):
        type = request.query_params.get('type', None)

    if request.query_params.get('size', None):
        size = request.query_params.get('size', None)

    if request.query_params.get('page', None):
        page = int(request.query_params.get('page', None))

    path = getattr(settings, "MEDIA_ROOT", None)+"/uploads/"
    if type is not None:
        if type == "thumbs" :
            path +=  "thumbnails/medium"

            if size == "small":
               path += "thumbnails/small"

        elif type == "cropped" and size is not None:
            path += "cropped/"+size

    img_list =os.listdir(path)
    img_list = [file for file in img_list if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif"))]

    # manage pagination
    pagemax = math.ceil(len(img_list)/PAGE_SIZE)

    if page is not None:

        if page > pagemax:
            page = pagemax

        if page < 1:
            page = 1

        startIndex = (page - 1)*10;

        stopindex = 0
        if len(img_list) < page*PAGE_SIZE:
            stopindex = len(img_list)
        else:
            stopindex = page*PAGE_SIZE

        img_list = img_list[startIndex:stopindex]

    data = { 'imgList' : img_list, 'page_max':pagemax}

    return Response(data, status.HTTP_200_OK)
