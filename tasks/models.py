# coding=utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

from classes.models import Pupil, Teacher


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "{name} (Тема № {num})".format(name=self.name, num=self.id)

    def get_url(self):
        return reverse('tasks:tasks_by_category', args=[self.id, 0])


class TheoryEntry(models.Model):
    category = models.ForeignKey(Category, related_name='theories')
    picture = models.ImageField(blank=True)
    text = models.TextField()

    def __unicode__(self):
        return u'Теория {num} по теме "{theme}"'.format(num=self.id, theme=self.category)


class SolvedTask(models.Model):
    category = models.ForeignKey(Category, related_name='solutions')
    picture = models.ImageField(blank=True,)
    question = models.TextField()
    solution = models.TextField()
    answer = models.CharField(max_length=255)

    def __unicode__(self):
        return u'Пример {num} по теме "{theme}"'.format(num=self.id, theme=self.category)


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
    picture = models.ImageField(blank=True, upload_to='media/')
    text = models.TextField()
    answer = models.CharField(max_length=255)
    theory = models.ForeignKey(TheoryEntry, related_name='tasks', null=True, blank=True)
    example = models.ForeignKey(SolvedTask, related_name='tasks', null=True, blank=True)

    def __unicode__(self):
        return u'Задача {}. {}...'.format(self.id, self.text[:150])

    def get_url(self):
        return reverse('tasks:show_task', args=[self.id])


class Attempt(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, related_name='attempts')
    pupil = models.ForeignKey(Pupil, related_name='attempts')
    answer = models.CharField(max_length=255)
    mark = models.IntegerField(default=None, null=True)

    def get_url(self):
        return reverse('tasks:show_attempt', args=[self.id])

    def __unicode__(self):
        return "Ответ {answer} на азадачу {task}".format(answer=self.answer, task=self.task.id)


class Homework(models.Model):
    pupil = models.ForeignKey(Pupil, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, related_name='homeworks')
    tasks = models.ManyToManyField(Task, related_name='homeworks_in', blank=True)
    is_open = models.BooleanField(default=True)

    def is_answered_full(self):
        for task in self.tasks.objects.all():
            if not task.attempts.objects.filter(pupil__is=self.pupil):
                return False
        return True

    def __unicode__(self):
        return u"Домашнее задание {id} от учителя {teacher}".format(id=self.id, teacher=self.teacher)
