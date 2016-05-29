from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from classes.models import Teacher, Pupil

from models import Category, Task, Attempt


class CreateCategory(UserPassesTestMixin, CreateView):
    model = Category

    def test_func(self):
        try:
            ppl = self.request.user.teacher
            if ppl is not None:
                return True
        except Teacher.DoesNotExist:
            return False


class CreateTask(UserPassesTestMixin, CreateView):
    model = Task

    def test_func(self):
        return self.request.user.classUser.is_teacher


class SolutionAttempt(UserPassesTestMixin, CreateView):
    model = Attempt

    def test_func(self):
        try:
            ppl = self.request.user.pupil
            if ppl is not None:
                return True
        except Pupil.DoesNotExist:
            return False

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


class CategoryTasks(ListView):
    template_name = 'tasks/category_tasks.html'

    def get_queryset(self):
        return Task.objects.filter(category_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(CategoryTasks, self).get_context_data()
        category = Category.objects.get(pk=self.kwargs["pk"])
        context['category'] = category
        return context
