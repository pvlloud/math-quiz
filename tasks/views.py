from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from classes.models import Teacher, Pupil
from classes.views import UserIsPupilMixin, UserIsTeacherMixin

from models import Category, Task, Attempt, Homework


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


class MarkAttempt(UserPassesTestMixin, UpdateView):
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
        return reverse('classes:show_pupil', args=[self.object.pupil.id])


class CategoryList(ListView):
    model = Category
    template_name = "tasks/category_list.html"


class CreateHomework(UserPassesTestMixin, CreateView):
    model = Homework
    fields = []

    def get_success_url(self):
        return reverse('tasks:category_list')

    def test_func(self):
        is_teacher = False
        try:
            this_user = self.request.user.teacher
            if this_user is not None:
                is_teacher = True
        except Teacher.DoesNotExist:
            return is_teacher
        can_create = this_user.can_create_homework
        return can_create and is_teacher

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.pupil = Pupil.objects.get(pk=self.kwargs["pupil"])
        obj.teacher = self.request.user.teacher
        return super(CreateHomework, self).form_valid(obj)


class TeacherHasOpenHomeworkMixin(UserPassesTestMixin):

    def test_func(self):
        is_teacher = False
        try:
            any_user = self.request.user.teacher
            if any_user is not None:
                is_teacher = True
        except Teacher.DoesNotExist:
            return is_teacher
        can_add = False
        for homework in any_user.homeworks.all():
            if homework.is_open:
                can_add = True
        return can_add and is_teacher


class AddTaskToHomework(TeacherHasOpenHomeworkMixin, UpdateView):
    model = Homework
    fields = []

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.tasks.add(Task.objects.get(pk=self.kwargs["task"]))
        return super(AddTaskToHomework, self).form_valid(obj)

    def get_success_url(self):
        return reverse('tasks:tasks_by_category', args=[Task.objects.get(pk=self.kwargs["task"]).category.id, 0])


class CloseHomework(TeacherHasOpenHomeworkMixin, UpdateView):
    model = Homework
    fields = []

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_open = False
        return super(CloseHomework, self).form_valid(obj)

    def get_success_url(self):
        return '/classes/profile'


class ShowHomework(UserPassesTestMixin, ListView):
    template_name = 'tasks/show_homework.html'

    def test_func(self):
        try:
            this_user = self.request.user.pupil
        except Pupil.DoesNotExist:
            try:
                this_user = self.request.user.teacher
            except Teacher.DoesNotExist:
                return False
        can_see = Homework.objects.get(pk=self.kwargs["homework"]) in this_user.homeworks.all()
        return can_see

    def get_queryset(self):
        homework_tasks = Homework.objects.get(pk=self.kwargs["homework"]).tasks.all()
        return homework_tasks

    def get_context_data(self, **kwargs):
        context = super(ShowHomework, self).get_context_data()
        homework = Homework.objects.get(pk=self.kwargs["homework"])
        context['homework'] = homework
        attempts = []
        for task in homework.tasks.all():
            atts = Attempt.objects.filter(pupil=homework.pupil, task=task)
            if atts:
                attempts.append(atts[0])
            else:
                attempts.append(task)
        context['homework_objects'] = attempts
        return context
