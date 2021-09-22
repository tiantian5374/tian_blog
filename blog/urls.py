from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # 主页
    path('', views.IndexView.as_view(), name='index'),
    # 详情页
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    # 归档栏
    path('archives/<int:year>/<int:month>', views.ArchiveView.as_view(),
         name='archive'),
    # 分类栏
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    # 标签栏
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
]
