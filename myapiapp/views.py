from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, OptionSerializer, QuestionSerializer, QuestionListSerializer, VoteSerializer
from myapp.models import Options, Question
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions


class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=True).all()
    serializer_class = UserSerializer


class OptionsViewSet(viewsets.ModelViewSet):
    queryset = Options.objects.all()
    serializer_class = OptionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionSerializer
        return QuestionListSerializer


class VoteView(generics.UpdateAPIView):
    serializer_class = VoteSerializer
    queryset = Options.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        question = Question.objects.get(id=data['question_id'])
        selected_option = Options.objects.get(id=data['answer'])
        for option in question.options_set.all():
            if request.user in option.votes.all():
                return Response({"message": "Already voted this question"})
        # if the user not vote the question then add vote
        selected_option.votes.add(request.user)
        selected_option.save()
        return Response({"message": "question is answered successfully"})


class ResultView(generics.GenericAPIView):
    pass
