from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import Http404


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import signals

from .models import Question, Choice
from .forms import QuestionForm
from django.http import HttpResponse
from django.views import View

from django.views.decorators.cache import cache_page
from .jobs import increase_view_count


# Create your views here.

def logging_callback(**kwargs):
    print(f"Log: {kwargs}")

# signals.pre_init.connect(logging_callback)
# signals.post_init.connect(logging_callback)
# signals.pre_save.connect(logging_callback)
# signals.post_save.connect(logging_callback)

@cache_page(5)
def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {'latest_question_list': questions}
    return render(request, 'polls/index.html', context)

# def detail(request, question_id: int):
#     try:
#         question = Question.objects.get(id=question_id)
#     except Question.DoesNotExist:
#         raise Http404('Question does not exists')
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)

def detail(request, question_id: int):
    # increase_view_count.delay(question_id)
    question = get_object_or_404(Question, id=question_id, pub_date__lte=timezone.now())
    increase_view_count.delay(question)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)


# from django.db import transaction
#
# @transaction.non_atomic_requests
def vote(request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choices.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'error_message': "You didn't select a choice",
            'question': question,
        })
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', question.id)


def results(request, question_id: int):
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}
    return render(request, 'polls/results.html', context)


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            pub_date = form.cleaned_data['publication_date']
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()
            for choice_text in form.cleaned_data['choices'].split('\n'):
                question.choices.create(choice_text=choice_text, votes=0)
            return redirect('polls:detail', question.id)
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})


