from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')  # 控制页面显示的字段

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 展示该分类下有多少篇文章
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 通过给obj.owner赋值达到设置owner的目的，request.user为当前登录的用户，未登录时user是匿名用户对象
    # form 是页面提交过来的表单之后的对象
    # change 用于标记本次保存的数据是新增还是更新


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''

    title = '分类过滤器'  # 展示标题
    parameter_name = 'owner_category'  # 查询时url参数的名字

    # 返回要展示的内容和查询用的id
    # 例如url后面Query部分是 ?owner_category=1 此时过滤器拿到的id就是1
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    # 根据url Query的内容返回列表页数据
    # QuerySet是列表页所有展示数据的合集，即post的数据集
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = (
        'title', 'category', 'status', 'created_time', 'operator', 'owner'
    )  # 配置列表显示哪些字段
    list_display_links = []  # 配置哪些字段可以作为链接，点击可以进入编辑
    list_filter = ['category', ]  # 配置页面过滤器，需要通过哪些字段过滤列表页
    search_fields = ['title', 'category_name']  # 配置搜索字段
    actions_on_top = True  # 动作相关配置，是否展示在顶部
    actions_on_bottom = True  # 动作相关配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存编辑编辑并新建是否在顶部展示
    exclude = ('owner',)  # 自动赋值当前用户
    # fields = (
    #     ('category', 'title'),
    #     'desc', 'status', 'content', 'tag',
    # )
    #  控制页面布局
    fieldsets = (
        ('基础配置', {
            'discription': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('clooapse',),
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        # 自定义函数可以返回html页面但是需要format_html函数处理
        # reverse 可以根据名称解析出url地址
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'  # 指定表头的展示方案

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js')