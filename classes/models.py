from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pupil(models.Model):
    user = models.OneToOneField(User, related_name='classUser')

    def __str__(self):
        return "Pupil " + self.user.username

    @property
    def is_teacher(self):
        return False

    @property
    def is_pupil(self):
        return True


class Teacher(models.Model):
    user = models.OneToOneField(User, related_name='classUser')
    keyword = models.CharField(max_length=256)

    pupils = models.ManyToManyField(Pupil, related_name="teachers")

    def __str__(self):
        return "Teacher " + self.user.username

    @property
    def is_teacher(self):
        return True

    @property
    def is_pupil(self):
        return False
