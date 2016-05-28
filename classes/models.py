from __future__ import unicode_literals

from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pupil(models.Model):
    user = models.OneToOneField(User)
    sessions_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Pupil " + self.user.username


def login_pupil(sender, request, user, **kwargs):
    try:
        user.pupil.sessions_number += 1
        user.pupil.save()
    except Pupil.DoesNotExist:
        return 0

user_logged_in.connect(login_pupil)


class Teacher(models.Model):
    user = models.OneToOneField(User)
    keyword = models.CharField(max_length=256)

    pupils = models.ManyToManyField(Pupil, related_name="teachers")

    def __str__(self):
        return "Teacher " + self.user.username
