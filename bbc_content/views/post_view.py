__author__ = 'Bertrand'

from mezzanine.blog.models import BlogPost
from bbc_content.views.serializers.content_serializers import BlogPostDescriptionSerializer,BlogPostDetailSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly

class PostList(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDescriptionSerializer

class PostCreate(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlogPostDetailSerializer

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)

class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer

 # list all assets
"""
    def post(request):
        serializer = BlogPostDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""