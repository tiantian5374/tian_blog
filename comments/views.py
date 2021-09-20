from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    # 一个评论只能属于一篇文章
    post = get_object_or_404(Post, pk=post_pk)
    # django 将用户提交数据封装在 request.POST 中，这是一个类字典对象
    # 构造CommentForm实例，生成了绑定用户数据的表单
    form = CommentForm(request.POST)

    # 表单合法
    if form.is_valid():
        # 仅生成评论实例，不提交到数据库
        comment = form.save(commit=False)
        # 将评论与被评的文章关联
        comment.post = post
        # 提交到数据库
        comment.save()
        # 显示提示信息
        messages.add_message(request, messages.SUCCESS, '评论发表成功！',
                             extra_tags='success')
        return redirect(post)

    # 表单不合法
    #
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR,
                         '评论发表失败！请修改表单中的错误后重新提交。',
                         extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
