from django.contrib import admin

# Register your models here.
from .models import Question, Options
admin.site.register(Question)
admin.site.register(Options)
