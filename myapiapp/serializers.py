from django.contrib.auth.models import User
from rest_framework import serializers
from myapp.models import Options, Question
import logging

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['url', 'text', 'votes', 'question_id']


class QuestionListSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField(method_name='get_author_username')

    class Meta:
        model = Question
        fields = ['url', 'text', 'datetime', 'author_username', 'options_set']
        depth = 0

    def get_author_username(self, question):
        return question.author.username


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['url', 'text', 'datetime', 'options_set']
        depth = 1


class VoteSerializer(serializers.Serializer):
    answer = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)

    def validate_question_id(self, value):
        try:
            question = Question.objects.get(id=value)
        except Question.DoesNotExist as ex:
            raise serializers.ValidationError("Should be a valid question id")
        return value

    def validate_answer(self, value):
        try:
            selected_option = Options.objects.get(id=value)
        except Options.DoesNotExist as ex:
            raise serializers.ValidationError("Should be a valid option id")
        return value

    def validate(self, data):
        question_id = data['question_id']
        answer = data['answer']
        # if isinstance(question_id, serializers.ValidationError) or isinstance(answer, serializers.ValidationError):
        #     return data
        try:
            question = Question.objects.get(id=question_id)
            selected_option = Options.objects.get(id=answer)
        except Exception as ex:
            # logging.exception(ex)
            raise serializers.ValidationError(str(ex))
        found = False
        options = question.options_set.all()
        for option in options:
            if option.id == selected_option.id:
                found = True
                break
        if not found:
            raise serializers.ValidationError("selected option must be inside question")
        return data