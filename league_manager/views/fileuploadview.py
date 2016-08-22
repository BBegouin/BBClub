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

@method_decorator(csrf_exempt, name='post')
class FileUploadView(APIView):
    parser_classes = (MultiPartParser,FileUploadParser,FormParser,)
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FileUploadView, self).dispatch(*args, **kwargs)

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        dest = getattr(settings, "MEDIA_ROOT", None)+"/uploads/"

        # on supprime les espaces, les caractéres spéciaux etc. via une regexp
        striped_name = re.sub('[^A-Za-z0-9.]+', '', up_file.name)

        fs = FileSystemStorage(location=dest)
        available_name = fs.get_available_name(striped_name)
        print(available_name)

        destination = open(dest + available_name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)

        destination.close()

        static_url = getattr(settings, "STATIC_URL", None)
        dest = getattr(settings, "MEDIA_ROOT", None)
        return Response(static_url+"media/uploads/"+available_name, status.HTTP_201_CREATED)
