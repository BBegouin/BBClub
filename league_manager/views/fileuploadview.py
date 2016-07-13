__author__ = 'Bertrand'

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

@method_decorator(csrf_exempt, name='post')
class FileUploadView(APIView):
    parser_classes = (MultiPartParser,FileUploadParser,FormParser,)
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(FileUploadView, self).dispatch(*args, **kwargs)

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        dest = getattr(settings, "MEDIA_ROOT", None)
        print(dest)

        destination = open(dest +"/uploads/" + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)

        destination.close()

        # ...
        # do some stuff with uploaded file
        # ...
        return Response(up_file.name, status.HTTP_201_CREATED)
