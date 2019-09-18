from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post, Category
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


# class PostViewSet(viewsets.ModelViewSet):
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    '''提供文章接口'''
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    # permission_classes = [IsAdminUser]  # 写入时的权限矫验

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer  # 重新设置，达到不同接口使用不同Serializer的目的
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request,*args,**kwargs)


