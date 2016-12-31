__author__ = 'Bertrand'
from rest_framework import viewsets
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from mezzanine.blog.models import BlogPost
from django_comments.models import Comment
from bbc_content.views.serializers.content_serializers import CommentListSerializer,CommentCreateSerializer

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = Comment.objects.all()

    def get_queryset(self):
        """
        on filtre selon le status, parametre optionnel de requête get
        """
        user_id = self.request.query_params.get('user_id', None)
        object_id = self.request.query_params.get('object_id', None)
        if user_id is not None:
            queryset = Comment.objects.filter(user__id=user_id)
        elif object_id is not None:
            queryset = Comment.objects.filter(object_pk=object_id)
        else:
            queryset = Comment.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list'\
            or self.action == 'retrieve' \
            or self.action == 'update'\
            or self.action == 'destroy':
                return CommentListSerializer
        elif self.action == 'create':
                return CommentCreateSerializer
