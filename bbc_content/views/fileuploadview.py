__author__ = 'Bertrand'

import re
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
from PIL import Image

@method_decorator(csrf_exempt, name='post')
class FileUploadView(APIView):
    parser_classes = (MultiPartParser,FileUploadParser,FormParser,)
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FileUploadView, self).dispatch(*args, **kwargs)

    """
    Create a thumbnail of a given file
    """
    def create_thumbnail(self,filepath,filename,target_width):
        # une fois que le fichier est présent, on crée une miniature

        dest = getattr(settings, "MEDIA_ROOT", None)+"/uploads/thumbnails/medium/"

        # on garde le nom original afin d'avoir une correspondance avec l'image originale
        outfile = dest + filename
        try:
            im = Image.open(filepath)
            im.thumbnail(target_width, Image.ANTIALIAS)
            im.save(outfile)
        except IOError:
            print("cannot create thumbnail for '%s'" % filename)

    """
    Upload a given file, mainly used for image files
    """
    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        dest = getattr(settings, "MEDIA_ROOT", None)+"/uploads/"

        # on supprime les espaces, les caractéres spéciaux etc. via une regexp
        striped_name = re.sub('[^A-Za-z0-9.]+', '', up_file.name)

        # on trouve un nom disponible pour éviter les collisions
        fs = FileSystemStorage(location=dest)
        available_name = fs.get_available_name(striped_name)

        filePath = dest + available_name;
        destination = open(filePath, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)

        destination.close()
        max_size = (250,250)
        self.create_thumbnail(filePath,available_name,max_size)

        static_url = getattr(settings, "STATIC_URL", None)
        return Response(static_url+"media/uploads/"+available_name, status.HTTP_201_CREATED)
