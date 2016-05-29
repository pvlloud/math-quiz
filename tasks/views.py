from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from classes.models import Teacher, Pupil
from classes.views import UserIsPupilMixin, UserIsTeacherMixin

from models import Category, Task, Attempt


class CreateCategory(LoginRequiredMixin, UserIsTeacherMixin, CreateView):
    model = Category
    fields = ['name']
    success_url = "/tasks/category_list"


class CreateTask(LoginRequiredMixin, UserIsTeacherMixin, CreateView):
    model = Task
    fields = ['category', 'level', 'picture', 'text', 'answer']
    success_url = "/tasks/category_list"
    template_name = "tasks/create_task.html"


class SolutionAttempt(LoginRequiredMixin, UserIsPupilMixin, CreateView):
    model = Attempt
    fields = ['answer']

    def get_success_url(self):
        return reverse('tasks:tasks_by_category', args=[Task.objects.get(pk=self.kwargs["pk"]).category_id, 0])

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.pupil = self.request.user.pupil
        obj.task = Task.objects.get(pk=self.kwargs["pk"])
        return super(SolutionAttempt, self).form_valid(obj)

    def get_context_data(self, **kwargs):
        context = super(SolutionAttempt, self).get_context_data()
        context['task'] = self.initial['task']
        return context


class CategoryLevelTasks(ListView):
    template_name = 'tasks/category_tasks.html'

    def get_queryset(self):
        category_tasks = Task.objects.filter(category_id=self.kwargs["pk"])
        if int(self.kwargs['level']) == 0:
            return category_tasks
        return category_tasks.filter(level=self.kwargs['level'])

    def get_context_data(self, **kwargs):
        context = super(CategoryLevelTasks, self).get_context_data()
        category = Category.objects.get(pk=self.kwargs["pk"])
        context['category'] = category
        context['level'] = self.kwargs["level"]
        return context


class ShowTask(DetailView):
    model = Task
    template_name = "tasks/show_task.html"


class ShowAttempt(LoginRequiredMixin, UserIsTeacherMixin, DetailView):
    model = Attempt
    template_name = "tasks/show_attempt.html"


class MarkAttempt(UpdateView, UserPassesTestMixin):
    model = Attempt
    fields = ['mark']

    def test_func(self):
        is_teacher = False
        try:
            any_user = self.request.user.teacher
            if any_user is not None:
                is_teacher = True
        except Teacher.DoesNotExist:
            return is_teacher
        is_own = self.object.pupil in self.request.user.teacher.pupils.all()
        return is_own and is_teacher

    def get_success_url(self):
        return reverse('tasks:show_pupil', args=[self.object.pupil.id])


class CategoryList(ListView):
    model = Category
    template_name = "tasks/category_list.html"
