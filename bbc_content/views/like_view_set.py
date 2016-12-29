__author__ = 'Bertrand'
from rest_framework import viewsets
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from bbc_content.models.like import Like
from rest_framework import status
from bbc_content.views.serializers.content_serializers import LikeSerializer
from rest_framework.response import Response
from rest_framework.decorators import list_route

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = Like.objects.all()

    def get_queryset(self):
        """
        on filtre selon l'id utilisateur et/ou l'id de post, paramètres optionnels
        """
        post_id = self.request.query_params.get('post_id', None)
        user_id = self.request.query_params.get('user_id', None)
        if post_id is not None and user_id is not None:
            queryset = Like.objects.filter(post__id = post_id,user__id = user_id)
        elif post_id is not None:
            queryset = Like.objects.filter(post__id = post_id)
        elif user_id is not None:
            queryset = Like.objects.filter(user__id = user_id)
        else:
            queryset = Like.objects.all()
        return queryset

    @list_route(methods=['delete'],permission_classes=[IsOwnerOrAdminReadOnly])
    def dislike(self, request, *arg, **kwarg):

        post_id = self.request.query_params.get('post_id', None)
        user_id = self.request.query_params.get('user_id', None)
        if post_id is None or user_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if int(user_id) != int(request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = Like.objects.filter(post__id = post_id,user__id = user_id)
        # delete the selected item
        queryset.delete()
        # return deleted
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):

        if self.action == 'retrieve' \
            or self.action == 'update'\
            or self.action == 'partial_update'\
            or self.action == 'list'\
            or self.action == 'create'\
            or self.action == 'destroy':
            return LikeSerializer