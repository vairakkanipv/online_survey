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
    # votes is a list of Users, who voted for this option
    votes = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.__class__.__name__}({self.question and self.question.id}, {self.text})"

#
# class Vote(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     option = models.ForeignKey(Options, on_delete=models.CASCADE())
#     author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#
#     def __str__(self):
#         retutn f"{self.__class__.__name__}"
