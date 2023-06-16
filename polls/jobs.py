from django.shortcuts import render, redirect, get_object_or_404

from .models import Question, Choice
from django.http import HttpResponse
from django.views import View
from django_rq import job
from time import sleep
from django.db.models import F


# class IncreaseViewCount(View):
@job
def increase_view_count(question: Question):
    # question = get_object_or_404(Question, pk=question_id)
    question.view_count = F('view_count') + 1
    question.save(update_fields=['view_count'])
    return HttpResponse("View count increased")

