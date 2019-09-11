from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post
from .serializers import PostSerializer


# class PostViewSet(viewsets.ModelViewSet):
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]  # 写入时的权限矫验