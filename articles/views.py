from django.shortcuts import render, get_object_or_404, redirect
from .models import Articles, Author


def index(request):
    articles = Articles.objects.all()
    context = {'all_articles': articles}
    return render(request, 'articles/index.html', context)


def detail(request, article_id: int):
    article = get_object_or_404(Articles, id=article_id)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)

def author_detail(request, author_id: int):
    return render(request, 'articles/author_detail.html', {
        'author': get_object_or_404(Author, id=author_id),
    })


def like(request):
    assert request.method == 'POST'
    article_id = request.POST['article_id']
    article = get_object_or_404(Articles, id=article_id)
    article.like_count += 1
    article.save()
    return redirect('articles:detail', article.id)
