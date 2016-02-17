from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pupil(models.Model):
    user = models.OneToOneField(User)


class Teacher(models.Model):
    user = models.OneToOneField(User)
    keyword = models.CharField(max_length=256)
