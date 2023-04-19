from django.urls import path

from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('like/', views.like, name='like'),
]