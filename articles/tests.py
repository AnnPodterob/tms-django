from django.test import TestCase
from django.urls import reverse
from .views import Articles

# Create your tests here.

def create_article(title, text, author, like_count):
    return Articles.objects.create(title=title, text=text, author=author, like_count=like_count)


class ArticleModelTest(TestCase):
    def test_empty_page(self):
        article = self.client.get(reverse('articles:index'))
        self.assertEquals(article.status_code, 200)
        self.assertContains(article, 'There are no articles')

    def test_getting_to_the_context(self):
        article = create_article('title', 'text', 'author', 5)
        response = self.client.get(reverse('articles:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], [article])

    def test_response_status_404(self):
        article = create_article('title', 'text', 'author', 5)
        response = self.client.get(reverse('articles:detail', args=[article.id]))
        self.assertEquals(response.status_code, 404)

    def test_contains_text(self):
        article = create_article('title', 'text', 'author', 5)
        response = self.client.get(reverse('articles:detail', args=[article.id]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, article.text)

    def test_is_popylar(self):
        article = Articles(like_count=10000)
        self.assertTrue(article.is_popular())

    def test_is_no_popylar(self):
        article = Articles(like_count=1)
        self.assertFalse(article.is_popular())