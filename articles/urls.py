from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/like', views.like, name='like'),
    path('authors/<int:author_id>/', views.detail, name='author_detail'),
]
