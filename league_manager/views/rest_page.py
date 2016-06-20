__author__ = 'Bertrand'

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mezzanine.pages.models import Page
from league_manager.models.general_post import GeneralPost
from league_manager.models.pages.general_page import GeneralPage
from league_manager.serializer import PageSerializer
from league_manager.serializer import GeneralPostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated



@api_view(['GET','POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def page_list(request, format = None):

    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        pages = GeneralPage.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        pages = PageSerializer(data=data)
        if pages.is_valid():
            pages.save()
            return Response(pages.data, status=201)
        return Response(pages.errors, status=400)

@api_view(['GET','PUT','DELETE'])
def page_detail(request, pk, format = None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        page = Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PageSerializer(page)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = PageSerializer(page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        page.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def post(request, format = None):
    """
    Retrieve, update or delete a post
    """

    if request.method == 'GET':
        post = GeneralPost.objects.all()
        serializer = GeneralPostSerializer(post, many=True)
        return Response(serializer.data)