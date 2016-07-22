__author__ = 'Bertrand'

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


####################################
#
# check if call isauthenticated
#
####################################
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def CheckToken(request):
    return Response(status=status.HTTP_200_OK)
