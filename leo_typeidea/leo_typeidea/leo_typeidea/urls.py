"""leo_typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
# from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
import xadmin

from blog.views import (IndexView, PostDetailView, CategoryView,
                        TagView, SearchView, AuthorView)
from blog.apis import PostViewSet, CategoryViewSet
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from config.views import LinkListView
from comment.views import CommentView
from .autocomplete import CategoryAutocomplete, TagAutocomplete

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')

urlpatterns = [
                  url(r'^$', IndexView.as_view(), name='index'),
                  url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
                  url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
                  # url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name='post-detail'),
                  url(r'^api/', include(router.urls, namespace='api')),
                  url(r'^links/$', LinkListView.as_view(), name='links'),
                  url(r'^search/$', SearchView.as_view(), name='search'),
                  url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
                  url(r'^comment/$', CommentView.as_view(), name='comment'),
                  url(r'^rss|feed/', LatestPostFeed(), name='rss'),
                  url(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_'), sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
                  url(r'^admin/', xadmin.site.urls, name='xadmin'),
                  url(r'^api/docs/', include_docs_urls(title='leo_typeidea apis')),
                  url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
                  url(r'^tag-autocomplete/%', TagAutocomplete.as_view(), name='tag-autocomplete'),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^silk/',include('silk.urls',namespace='silk')),
    ]