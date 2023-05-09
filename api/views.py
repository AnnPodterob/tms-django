from django.shortcuts import render

from rest_framework import viewsets

from polls.models import Question, Choice
from shop.models import Category, Product
from articles.models import Author, Articles

from .serializers import QuestionSerializer, ChoiceSerializer
from .serializers import CategorySerializer, ProductSerializer
from .serializers import AuthorSerializer, ArticleSerializer



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related('articles')
    serializer_class = AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer