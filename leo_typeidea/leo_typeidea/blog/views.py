from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView,ListView

from .models import Post, Tag, Category
# from leo_typeidea.leo_typeidea.config.models import SideBar
from config.models import SideBar

# Create your views here.

class CommonViewMiXin:
    '''通用数据，基础数据'''
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1  # 每页的数据
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'

# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


class PostDetailView(CommonViewMiXin,DetailView):
    model = Post
    template_name = 'blog/detail/html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
# def post_datail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'log/detail.html', context=context)


class IndexView(CommonViewMiXin,ListView):
    '''首页'''
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html0'

class CategoryView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category,
        })
        return context
    def get_queryset(self):
        '''重写get_queryser方法，根据标签过滤'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # self.kwargs中的数据是从url定义中拿到的
        tag = get_object_or_404(Category, pk=tag_id)  # 快捷方式，获取一个对象的实例，获取到就返货，没有就报404
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写get_queryser方法，根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

