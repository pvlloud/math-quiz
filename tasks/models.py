# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from classes.models import Pupil


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    LEVEL_CHOICES = (
        (1, u'Уровень 1'),
        (2, u'Уровень 2'),
        (3, u'Уровень 3'),
        (4, u'Уровень 4'),
        (5, u'Уровень 5'),
    )

    category = models.ForeignKey(Category, related_name='tasks')
    level = models.IntegerField(choices=LEVEL_CHOICES)
    picture = models.ImageField(blank=True)
    text = models.TextField()
    answer = models.CharField(max_length=255)

    def __unicode__(self):
        return u'Задача {}'.format(self.id)


class Attempt(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, related_name='attempts')
    pupil = models.ForeignKey(Pupil, related_name='attempts')
    answer = models.CharField(max_length=255)
    mark = models.IntegerField(default=None)
