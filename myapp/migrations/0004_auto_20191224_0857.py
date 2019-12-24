# Generated by Django 2.2.7 on 2019-12-24 03:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_question_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='options',
            name='votes',
        ),
        migrations.AddField(
            model_name='options',
            name='votes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
