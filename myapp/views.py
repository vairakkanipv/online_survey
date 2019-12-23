from django.shortcuts import render,redirect
from .models import Question, Options
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm


class MyLoginView(LoginView):
    template_name = 'myapp/login.html'

    # def get(self, request):
    #     if request.user.is_authenticated:
    #         return redirect('myapp: question_list')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('myapp: question_list')
        return super(MyLoginView, self).dispatch(request, *args, **kwargs)


class MyLogoutView(LogoutView):
    next_page = "/login/"


class QuestionList(LoginRequiredMixin, generic.ListView):
    model = Question

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.all()


class QuestionDetail(LoginRequiredMixin, generic.DetailView):
    model = Question
    #template_name = 'myapp/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context['question']
        options = question.options_set.all()
        context['options'] = options
        return context

    # def get_queryset(self,question_id):
    #     question = Question.objects.get(id=question_id)
    #     return question.options_set.all()


# def question_detail(request, question_id):
#     try:
#         question = Question.objects.get(id=question_id)
#         options = question.options_set.all()
#     except Question.DoesNotExist:
#         return render(request, '404.html', {'message': 'Question Not Found with id {}'.format(question_id)})
#     else:
#         return render(request, 'question_detail.html', {'question': question, 'options': options})


def vote(request, question_id):
    '''
    - fetch question id
    - fetch option id
    - check question id is valid
    - check option id is one among the questions's option
    :param request:
    :return:
    '''
    # try:
    #     current_question_id = int(request.GET['question_id'])
    # except (ValueError, KeyError) as ex:
    #     print(ex)
    #     return HttpResponseRedirect(reverse('myapp:question_list'))
    current_question_id = question_id
    try:
        current_answer_id = int(request.GET['answer'])
    except (KeyError, ValueError) as ex:
        return HttpResponseRedirect(reverse('myapp:question_details', args=(current_question_id,)))
    #current_answer_id = option_id
    try:
        question = Question.objects.get(id=current_question_id)
    except Question.DoesNotExist as ex:
        print(ex)
        return HttpResponseRedirect(reverse('myapp:question_list'))

    try:
        selected_option = Options.objects.get(id=current_answer_id)
    except Options.DoesNotExist as ex:
        print(ex)
        return HttpResponseRedirect(reverse('myapp:question_details', args=(current_question_id,)))

    found = False
    options = question.options_set.all()
    for option in options:
        if(option.id == selected_option.id):
            found = True
            break

    if(found == True):
        selected_option.votes += 1
        selected_option.save()
        return HttpResponseRedirect(reverse('myapp:results', args=(current_question_id,)))
    else:
        return HttpResponseRedirect(reverse('myapp:question_details', args=(current_question_id,)))


def result(request,question_id):
    question = Question.objects.get(id=question_id)
    options = question.options_set.all()
    total_votes = 0
    for option in options:
        total_votes += option.votes
    return render(request, 'success.html', {'options': options, 'total_votes': total_votes})


class AddQuestion(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/add_question.html"

    def post(self, request):
        question_text = request.POST['question_text']
        options_text = [request.POST[option_key] for option_key in ['option1', 'option2', 'option3']]
        if not question_text.strip() or not all(text.strip() for text in options_text):
            return HttpResponseRedirect(reverse('myapp:question_list'))
        question = Question(text=question_text, datetime=timezone.now(), author_id=request.user.id)
        question.save()

        for option_text in options_text:
            option = Options(question_id=question.id, text=option_text)
            option.save()

        return HttpResponseRedirect(reverse('myapp:question_list'))


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = user.username # form.cleaned_data.get('username')
            return HttpResponseRedirect(reverse('myapp:question_list'))
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request=request, template_name="myapp/register.html", context={"form": form})

    form = UserCreationForm()
    return render(request=request,
                  template_name="myapp/register.html",
                  context={"form": form})


class RegisterView(generic.TemplateView):
    template_name = "myapp/register.html"

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('myapp:question_list'))
        else:
            return render(request=request, template_name=self.template_name, context={"form": form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserCreationForm()
        return context
