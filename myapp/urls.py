from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path('login/', views.login, name='loginurl'),
    path('', views.QuestionList.as_view(), name='question_list'),
    #path('question_detail/<int:question_id>', views.question_detail, name="question_details"),
    path('question_detail/<int:pk>', views.QuestionDetail.as_view(), name="question_details"),
    path('vote/<int:question_id>', views.vote, name="vote"),
    path('results/<int:question_id>',views.result, name='results'),
    path('add_question',views.AddQuestion.as_view(), name='add_question'),

]