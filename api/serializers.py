from polls.models import Question, Choice
from rest_framework import serializers
from shop.models import Category, Product
from articles.models import Articles, Author


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.HyperlinkedRelatedField(
        view_name='choice-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.HyperlinkedRelatedField(
        view_name='question-detail',
        read_only=True,
    )

    class Meta:
        model = Choice
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True,
    )

    class Meta:
        model = Product
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        view_name='article-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Author
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail',
        read_only=True,
    )

    class Meta:
        model = Articles
        fields = '__all__'