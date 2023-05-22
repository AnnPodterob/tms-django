from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet, basename='question')
router.register('choices', views.ChoiceViewSet, basename='choice')
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('authors', views.AuthorViewSet)
router.register('articles', views.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test', views.test_view)
]