from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice

from rest_framework.test import APITestCase
from articles.models import Author, Articles
from shop.models import Category, Product

class QuestionApiTest(TestCase):
    def test_empty_question_list(self):
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, [])

    def test_non_existent_question_id(self):
        response = self.client.get('/api/questions/1/')
        self.assertEquals(response.status_code, 404)

    def test_question_list(self):
        Question.objects.create(question_text='Text1', pub_date=timezone.now())
        Question.objects.create(question_text='Text2', pub_date=timezone.now())

        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data[0]['question_text'], 'Text1')
        self.assertEquals(data[1]['question_text'], 'Text2')

    def test_question_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())

        response = self.client.get(f'/api/questions/{question.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['question_text'], question.question_text)


class ChoiceApiTest(TestCase):
    def test_empty_choice_list(self):
        response = self.client.get('/api/choices/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, [])

    def test_non_existent_choice_id(self):
        response = self.client.get('/api/choices/1/')
        self.assertEquals(response.status_code, 404)

    def test_choice_list(self):
        Choice.objects.create(choice_text='Text1')
        Choice.objects.create(choice_text='Text2')

        response = self.client.get('/api/choices/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data[0]['choice_text'], 'Text1')
        self.assertEquals(data[1]['choice_text'], 'Text2')

    def test_choice_detail(self):
        choice = Choice.objects.create(choice_text='Text1')

        response = self.client.get(f'/api/choices/{choice.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['choice_text'], choice.choice_text)


class AuthorAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01'
        )

    def test_create_article(self):
        url = '/api/articles/'
        data = {
            'title': 'Test Article',
            'text': 'This is a test article.',
            'like_count': 0,
            'authors': [self.author.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Articles.objects.count(), 1)
        self.assertEqual(Articles.objects.get().title, 'Test Article')

class ArticlesAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01'
        )
        self.article = Articles.objects.create(
            title='Test Article',
            text='This is a test article.',
            like_count=0
        )
        self.article.authors.add(self.author)

    def test_update_article_put(self):
        url = f'/api/articles/{self.article.id}/'
        data = {
            'title': 'Updated Article',
            'text': 'This is an updated article.',
            'like_count': 1,
            'authors': [self.author.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article')
        self.assertEqual(self.article.text, 'This is an updated article.')
        self.assertEqual(self.article.like_count, 1)

    def test_update_article_patch(self):
        url = f'/api/articles/{self.article.id}/'
        data = {
            'title': 'Patched Article',
            'like_count': 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Patched Article')
        self.assertEqual(self.article.text, 'This is a test article.')
        self.assertEqual(self.article.like_count, 2)


class CategoryAPITest(APITestCase):
    def test_create_category(self):
        url = '/api/categories/'
        data = {
            'name': 'Test Category'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')

    def test_update_category_put(self):
        category = Category.objects.create(name='Test Category')
        url = f'/api/categories/{category.id}/'
        data = {
            'name': 'Updated Category'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Updated Category')

    def test_update_category_patch(self):
        category = Category.objects.create(name='Test Category')
        url = f'/api/categories/{category.id}/'
        data = {
            'name': 'Patched Category'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Patched Category')

class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_create_product(self):
        url = '/api/products/'
        data = {
            'category': self.category.id,
            'name': 'Test Product',
            'description': 'This is a test product.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_update_product_put(self):
        product = Product.objects.create(category=self.category, name='Test Product', description='This is a test product.')
        url = f'/api/products/{product.id}/'
        data = {
            'category': self.category.id,
            'name': 'Updated Product',
            'description': 'This is an updated product.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Product')
        self.assertEqual(product.description, 'This is an updated product.')

    def test_update_product_patch(self):
        product = Product.objects.create(category=self.category, name='Test Product', description='This is a test product.')
        url = f'/api/products/{product.id}/'
        data = {
            'name': 'Patched Product'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.name, 'Patched Product')