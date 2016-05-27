from __future__ import unicode_literals

from django.db import models

from classes.models import Pupil


class Category(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    category = models.ForeignKey(Category, related_name='tasks')
    level = models.IntegerField()
    picture = models.ImageField()
    text = models.TextField()
    answer = models.CharField(max_length=255)


class Attempt(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, related_name='attempts')
    pupil = models.ForeignKey(Pupil, related_name='attempts')
    answer = models.CharField(max_length=255)
    mark = models.IntegerField(default=None)
