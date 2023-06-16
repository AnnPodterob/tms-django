from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', db_index=True)
    view_count = models.IntegerField(default=0)
    # best_choice = models.OneToOneField('Choice', null=True, on_delete=models.SET_NULL, related_name='best_question')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        description='Published recently?',
        ordering='pub_date'
    )
    def was_published_recently(self):
        if not self.pub_date:
            return False
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # best_question = models.ManyToManyField(Question, related_name='best_questions')


    def __str__(self):
        return f'{self.question.question_text} : {self.choice_text}'

    @admin.display(
        description='Question Text',
        ordering='question__question_text'
    )
    def get_question_text(self):
        return self.question.question_text

