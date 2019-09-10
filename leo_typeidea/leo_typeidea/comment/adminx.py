from django.contrib import admin
from .models import Comment
from leo_typeidea.custom_site import custom_site
import xadmin
# Register your models here.

@xadmin.sites.register(Comment)  # 9.4新增site
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'target', 'nickname', 'content', 'website', 'created_time',
    )
