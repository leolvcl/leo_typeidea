from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter
import xadmin

from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from leo_typeidea.base_admin import BaseOwnerAdmin



# Register your models here.

class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')  # 控制页面显示的字段

    # 展示该分类下有多少篇文章
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    '''自定义过滤器只展示当前用户分类'''

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        # 确定字段是否需要被当前的过滤器处理
        return field.name == 'category'

    def __init__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        # 重新获取lookup_choice 根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]  # 配置列表显示哪些字段
    list_display_links = []  # 配置哪些字段可以作为链接，点击可以进入编辑

    # list_filter = ['CategoryOwnerFilter,' ]  # 配置页面过滤器，需要通过哪些字段过滤列表页
    list_filter = ['category']  # 此处是字段名
    search_fields = ['title', 'category_name']  # 配置搜索字段
    # save_on_top = True

    actions_on_top = True  # 动作相关配置，是否展示在顶部
    actions_on_bottom = True  # 动作相关配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存编辑编辑并新建是否在顶部展示
    exclude = ['owner', ]  # 自动赋值当前用户

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md'
            'content',
            'content_ck',
            'content_md',
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'  # 指定表头的展示方案

