from datetime import date

from django.db.models import Q,F
from django.core.cache import cache

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from .models import Post, Tag, Category
# from leo_typeidea.leo_typeidea.config.models import SideBar
from config.models import SideBar
from comment.forms import CommentForm
from comment.models import Comment


# Create your views here.

class CommonViewMixin:
    '''通用数据，基础数据'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    def get_navs(self):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

class IndexView(CommonViewMixin, ListView):
    '''首页'''
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
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
        tag = get_object_or_404(Tag, pk=tag_id)  # 快捷方式，获取一个对象的实例，获取到就返货，没有就报404
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写get_queryser方法，根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMixin, DetailView):
    # model = Post
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request,*args,**kwargs)
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        self.handle_visited()
        # 调试用
        # from django.db import connection
        # print(connection.queries)
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:{}:{}'.format(uid,self.request.path)
        uv_key = 'uv:{}:{}:{}'.format(uid,str(date.today()),self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)  # 一分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key,1,24*60*60)  # 24小时有效
        if increase_uv and increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path),
    #     })
    #     return context

class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):  # 控制数据源
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
# class PostListView(ListView):
#     queryset = Post.latest_posts()
#     paginate_by = 1  # 每页的数据
#     context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用object_list变量
#     template_name = 'blog/list.html'

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








