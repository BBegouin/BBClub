__author__ = 'Bertrand'


import os
import math
import base64
import re
from PIL import Image

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.files.storage import FileSystemStorage
from django.conf import settings


PAGE_SIZE = 8

def get_static_storage_url(request):
    domain = request.build_absolute_uri('/')[:-1]
    static_path = getattr(settings, "STATIC_URL", None)
    file_url = domain + static_path +"medias/uploads/"
    return file_url

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

    root_url = get_static_storage_url(request)

    img_list = [{"name":file,"url":root_url+file} for file in img_list]
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

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def crop_image(request):
    try:
        # variable definition
        file_to_crop = request.data['filename']
        top = int(request.data['top'])
        left = int(request.data['left'])
        width = int(request.data['width'])
        height = int(request.data['height'])
    except KeyError as e:
         return Response("filename, top,left,width,height shall be set",status.HTTP_400_BAD_REQUEST)

    if top < 0  or left < 0 or width <= 0 or height <= 0 :
       return Response("width and height shall be > 0",status.HTTP_400_BAD_REQUEST)

    computed_file_name = file_to_crop.rsplit('/', 1)[1]

    #
    file_path = getattr(settings, "MEDIA_ROOT", None)+"/uploads/"+computed_file_name
    try:
        with open(file_path) as file:
            pass
    except IOError as e:
        return Response(status.HTTP_404_NOT_FOUND)

    dest_file = getattr(settings, "MEDIA_ROOT", None)+"/uploads/cropped/"+computed_file_name
    img = Image.open(file_path)

    img2 = img.crop((top, left, width, height))
    img2.save(dest_file)

    static_url = getattr(settings, "STATIC_URL", None)
    cropped_file_url = static_url +"medias/uploads/cropped/"+ computed_file_name;
    domain = request.build_absolute_uri('/')[:-1]
    return Response(domain+cropped_file_url,status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def binary_upload(request):

    try:
        filename = request.data['filename']
        binary_img = request.data['payload']
    except KeyError as e:
         return Response("filename, and payload shall be set",status.HTTP_400_BAD_REQUEST)

    dest = getattr(settings, "MEDIA_ROOT", None)+"/uploads/cropped/"

    # on trouve un nom disponible pour éviter les collisions
    fs = FileSystemStorage(location=dest)
    filename = fs.get_available_name(filename)
    filePath = dest + filename;

    image_type, image_content = binary_img.split(',', 1)

    image_type = re.findall('data:image\/(\w+);base64', image_type)[0]
    with open(filePath, "wb") as f:
        f.write(base64_decode(image_content))

    static_url = getattr(settings, "STATIC_URL", None)
    domain = request.build_absolute_uri('/')[:-1]
    file_url = domain+static_url+"medias/uploads/cropped/"+filename
    img_data = {"url":file_url,"name":filename}

    return Response(img_data,status.HTTP_200_OK)

def base64_decode(s):
    """Add missing padding to string and return the decoded base64 string."""
    s = str(s).strip()
    try:
        return base64.b64decode(s)
    except TypeError:
        padding = len(s) % 4
        if padding == 1:
            print("Invalid base64 string: {}".format(s))
            return ''
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        return base64.b64decode(s)
