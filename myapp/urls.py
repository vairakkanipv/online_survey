from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='loginurl'),
    path('logout/', views.MyLogoutView.as_view(), name='logouturl'),
    path('', views.QuestionList.as_view(), name='question_list'),
    #path('question_detail/<int:question_id>', views.question_detail, name="question_details"),
    path('question_detail/<int:pk>', views.QuestionDetail.as_view(), name="question_details"),
    path('vote', views.VoteView.as_view(), name="vote"),
    path('results/<int:question_id>',views.ResultView.as_view(), name='results'),
    path('add_question',views.AddQuestion.as_view(), name='add_question'),
    path("register/", views.RegisterView.as_view(), name="register"),

]