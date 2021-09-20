from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 详情页
    path('post/<int:pk>/', views.detail, name='detail'),
    # 归档栏
    path('archives/<int:year>/<int:month>', views.archive, name='archive'),
    # 分类栏
    path('categories/<int:pk>', views.category, name='category'),
    # 标签栏
    path('tags/<int:pk>', views.tag, name='tag'),
]