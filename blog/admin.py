from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    # list_display不能显示多对多的属性
    list_display = ['title', 'created_time', 'modified_time', 'category',
                    'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


# 注册模型
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
