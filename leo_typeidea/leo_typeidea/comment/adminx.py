import xadmin

from .models import Comment

# Register your models here.

@xadmin.sites.register(Comment)  # 9.4新增site
class CommentAdmin():
    list_display = (
        'target', 'nickname', 'content', 'website', 'created_time',
    )
