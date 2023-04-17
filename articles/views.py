from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, Http404

# Create your views here.
from django.http import HttpRequest
from .models import Articles


def index(request: HttpRequest):
    articles = Articles.objects
    context = {'articles_list': articles}
    return render(request, 'articles/index.html', context)


def detail(request, article_id: int):
    article = get_object_or_404(Articles, id=article_id)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)



def like(request, article_id: int):
    article = get_object_or_404(Articles, id=article_id)
    article_id = request.POST['article_id']
    article.likes += 1
    article.save()
    return redirect('articles:detail', article_id)