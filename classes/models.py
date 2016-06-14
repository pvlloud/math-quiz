# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.signals import user_logged_in
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pupil(models.Model):
    user = models.OneToOneField(User)
    sessions_number = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'{} {}'.format(self.user.last_name, self.user.first_name)

    def calculate_rating(self):
        marked_attempts = self.attempts.filter(mark__isnull=False)
        marks = [int(marked_attempt.mark) for marked_attempt in marked_attempts]
        if marks:
            average = sum(marks)/float(len(marks))
            return average
        return 0

    def get_url(self):
        return reverse('classes:show_pupil', args=[self.id])

    def get_homeworks(self):
        return self.homeworks.all().filter(is_open=False)


def login_pupil(sender, request, user, **kwargs):
    try:
        user.pupil.sessions_number += 1
        user.pupil.save()
    except Pupil.DoesNotExist:
        return 0

user_logged_in.connect(login_pupil)


class Teacher(models.Model):
    user = models.OneToOneField(User)
    about = models.TextField(blank=True)
    keyword = models.CharField(max_length=256)

    pupils = models.ManyToManyField(Pupil, related_name="teachers", blank=True)

    def __unicode__(self):
        return u'{} {}'.format(self.user.last_name, self.user.first_name)

    def get_url(self):
        return reverse('classes:show_teacher', args=[self.id])

    def can_create_homework(self):
        can_create = True
        for homework in self.homeworks.all():
            if homework.is_open:
                can_create = False
        return can_create

    def get_open_homework(self):
        for homework in self.homeworks.all():
            if homework.is_open:
                return homework
        return None


class TeacherRegistryKeyword(models.Model):
    keyword = models.CharField(max_length=255)

    def __unicode__(self):
        return self.keyword
