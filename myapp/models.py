from django.db import models


# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=100)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.text


class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.text,self.question and self.question.id)
