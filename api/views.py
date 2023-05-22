from django.shortcuts import render

from rest_framework import viewsets, filters, pagination
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from polls.models import Question, Choice
from shop.models import Category, Product
from articles.models import Author, Articles

from .serializers import QuestionSerializer, ChoiceSerializer
from .serializers import CategorySerializer, ProductSerializer
from .serializers import AuthorSerializer, ArticleSerializer


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def test_view(request):
    my_param_1 = request.query_params.get('my_param_1')
    my_param_2 = request.query_params.get('my_param_2')

    data = {'question_count': my_param_1, 'choice_count': my_param_2}
    return Response(data)

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'question_text', 'pub_date']
    search_fields = ['id', 'question_text', 'pub_date']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Question.objects.prefetch_related('choices')
        min_choice_count = self.request.query_params.get('min_choice_count')
        max_choice_count = self.request.query_params.get('max_choice_count')
        if min_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__gte=min_choice_count)
        if max_choice_count is not None:
            queryset = queryset.annotate(choice_count=Count('choices')).filter(choice_count__lte=max_choice_count)
        return queryset


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'choice_text', 'votes']
    search_fields = ['id', 'choice_text', 'votes']
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Choice.objects.all()
        question_text = self.request.query_params.get('question_text')
        if question_text is not None:
            queryset = queryset.filter(question__question_text__icontains=question_text)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.prefetch_related('articles')
    serializer_class = AuthorSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer