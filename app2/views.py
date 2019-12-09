from django.shortcuts import render
from .models import Question, Options
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def login(request):
    return render(request, 'login.html')


def question_list(request):
    if request.method == "GET":
        questions = Question.objects.all()
        return render(request, 'question_list.html', {'questions': questions})
    else:
        return render(request, '404.html', {'message': 'Page not Found. 404'})


def question_detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        options = question.options_set.all()
    except Question.DoesNotExist:
        return render(request, '404.html', {'message': 'Question Not Found with id {}'.format(question_id)})
    else:
        return render(request, 'question_detail.html', {'question': question, 'options': options})


def vote(request, question_id):
    '''
    - fetch question id
    - fetch option id
    - check question id is valid
    - check option id is one among the questions's option
    :param request:
    :return:
    '''
    # get the marked Option ID
    try:
        current_answer_id = int(request.GET['answer'])
    except (KeyError, ValueError) as ex:
        return HttpResponseRedirect(reverse('myapp:question_details', args=(question_id,)))
    # get the Question using question_id
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist as ex:
        print(ex)
        return HttpResponseRedirect(reverse('myapp:question_list'))

    try:
        selected_option = Options.objects.get(id=current_answer_id)
    except Options.DoesNotExist as ex:
        print(ex)
        return HttpResponseRedirect(reverse('myapp:question_details', args=(question_id,)))

    options = question.options_set.all()
    if(selected_option in options):
        selected_option.votes += 1
        selected_option.save()
        return HttpResponseRedirect(reverse('myapp:results', args=(question_id,)))
    else:
        return HttpResponseRedirect(reverse('myapp:question_details', args=(question_id,)))


def result(request, question_id):
    question = Question.objects.get(id=question_id)
    options = question.options_set.all()
    total_votes = 0
    for option in options:
        total_votes += option.votes
    # total_votes = sum(option.votes for option in options)
    return render(request, 'success.html', {'options': options, 'total_votes': total_votes})


