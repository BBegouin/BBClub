__author__ = 'Bertrand'
from rest_framework import viewsets
from core.permissions.owner_or_admin import IsOwnerOrAdminReadOnly
from mezzanine.blog.models import BlogPost
from bbc_content.views.serializers.content_serializers import BlogPostDescriptionSerializer,BlogPostDetailSerializer,BlogPostCreateSerializer

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrAdminReadOnly,)
    queryset = BlogPost.objects.all()

    def get_queryset(self):
        """
        on filtre selon le status, parametre optionnel de requête get
        """
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = BlogPost.objects.filter(status=status)
        else:
            queryset = BlogPost.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostDescriptionSerializer
        elif self.action == 'retrieve' \
            or self.action == 'update'\
            or self.action == 'partial_update'\
            or self.action == 'destroy':
            return BlogPostDetailSerializer
        elif self.action == 'create':
            return BlogPostCreateSerializer