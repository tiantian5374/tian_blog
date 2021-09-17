from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """分类模型"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章模型，包含 标题，标签，分类，作者，创建时间，修改时间，摘要，主体

    """
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # blank=True 代表这一项可以为空，非必填项
    excerpt = models.CharField(max_length=200, blank=True)
    # 一篇文章只对应一个分类用外键关联外模型，一篇文章对应多标签用多对多标签
    # on_delete=models.CASCADE 代表删除时，关联的所有文章都删除
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
