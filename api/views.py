from django.shortcuts import render

from rest_framework import viewsets
from polls.models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer