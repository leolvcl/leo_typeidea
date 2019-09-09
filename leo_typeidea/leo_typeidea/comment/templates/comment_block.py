from django import template

from comment.models import Comment
from comment.foems import CommentForm

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target)

    }
