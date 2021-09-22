from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
import markdown
import re

from .models import Post, Category, Tag


class IndexView(ListView):
    # 主页的类视图
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
"""
def index(request):
    # 主页函数
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""


class PostDetailView(DetailView):
    # 详情页函数
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request, *args, **kwargs):
        # 覆写get方法，增加阅读量+1
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object方法的目的是需要对body渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r"<div class='toc'>\s*<ul>(.*)</ul>\s*</div>",
                      md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
"""
def detail(request, pk):
    # 详情页函数
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})
"""


class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # 筛选出该归档的所有文章
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month'))
"""
def archive(request, year, month):
    # 归档栏函数
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""


class CategoryView(ListView):
    # 分类栏的类视图
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        # 筛选出该分类的所有文章
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
"""
def category(request, pk):
    # 分类栏
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""


class TagView(ListView):
    # 标签栏的类视图
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=t)
"""
def tag(request, pk):
    # 标签栏
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})
"""