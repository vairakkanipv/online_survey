from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.__class__.__name__}({self.author.username}, {self.text})"
        # return f"{self.__class__.__name__}({self.text})"


class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.__class__.__name__}({self.question and self.question.id}, {self.text})"

