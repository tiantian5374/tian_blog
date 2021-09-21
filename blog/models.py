from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags

import markdown


class Category(models.Model):
    """分类模型"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章模型，包含 标题，标签，分类，作者，创建时间，修改时间，摘要，主体

    """
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间')
    modified_time = models.DateTimeField('修改时间')
    # blank=True 代表这一项可以为空，非必填项
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 一篇文章只对应一个分类用外键关联外模型，一篇文章对应多标签用多对多标签
    # on_delete=models.CASCADE 代表删除时，关联的所有文章都删除
    category = models.ForeignKey(Category, verbose_name='分类',
                                 on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 重写save方法
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 实例化markdown类，用于渲染body，摘要不需要目录，不需要目录拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # strip_tags 去除全部html标签
        self.excerpt = strip_tags(md.convert(self.body))
        self.excerpt = (self.excerpt[:54] + ' . . .') \
                        if len(self.excerpt) > 54 else self.excerpt[:54]

        super().save(*args, **kwargs)

    # 定义详情页路径
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
