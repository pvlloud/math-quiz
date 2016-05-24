from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin

from models import Category, Task, Attempt


class CreateCategory(UserPassesTestMixin, CreateView):
    model = Category

    def test_func(self):
        return self.request.user.classUser.is_teacher


class CreateTask(UserPassesTestMixin, CreateView):
    model = Task

    def test_func(self):
        return self.request.user.classUser.is_teacher


class SolutionAttempt(UserPassesTestMixin, CreateView):
    model = Attempt

    def test_func(self):
        return self.request.user.classUser.is_pupil

    def get_initial(self):
        initial = super(SolutionAttempt, self).get_initial()
        initial = initial.copy()
        initial['pupil'] = self.request.user.classUser
        initial['task'] = Task.objects.get(pk=self.kwargs["pk"])
        return initial

    def get_context_data(self, **kwargs):
        context = super(SolutionAttempt, self).get_context_data()
        context['task'] = self.initial['task']
        return context
