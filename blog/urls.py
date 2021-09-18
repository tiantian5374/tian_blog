from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 详情页
    path('post/<int:pk>/', views.detail, name='detail'),
]