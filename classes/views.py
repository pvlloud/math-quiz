from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from forms import UserRegistrationForm, PupilKeywordForm
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from models import Teacher, Pupil, TeacherRegistryKeyword


class UserIsTeacherMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            any_user = self.request.user.teacher
            if any_user is not None:
                return True
        except Teacher.DoesNotExist:
            return False


class UserIsPupilMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            any_user = self.request.user.pupil
            if any_user is not None:
                return True
        except Pupil.DoesNotExist:
            return False


class RegisterView(FormView):
    template_name = 'classes/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('classes:register')

    def form_valid(self, form):
        # Create a new user object but avoid saving it yet
        new_user = form.save(commit=False)
        # Set the chosen password
        new_user.set_password(
            form.cleaned_data['password'])
        # Save the User object
        new_user.save()
        if TeacherRegistryKeyword.objects.get(keyword=form.cleaned_data['if_teacher_keyword']):
            teacher = Teacher.objects.create(user=new_user)
        else:
            pupil = Pupil.objects.create(user=new_user)
        return super(RegisterView, self).form_valid(form)


class BindPupilToTeacher(LoginRequiredMixin, UserIsPupilMixin, FormView):
    login_url = reverse_lazy('classes:login')
    template_name = 'classes/pupil_to_teacher_keyword.html'
    form_class = PupilKeywordForm

    def form_valid(self, form):
        teacher = Teacher.objects.get(pk=self.kwargs["pk"])
        if form.cleaned_data['keyword'] == teacher.keyword:
            teacher.pupils.add(self.request.user.pupil)
        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong Keyword!')
            return self.form_invalid(form)
        return super(BindPupilToTeacher, self).form_valid(form)


class ShowTeacher(LoginRequiredMixin, UserIsPupilMixin, DetailView):
    model = Teacher
    template_name = 'classes/show_teacher.html'

    def get_context_data(self, **kwargs):
        context = super(ShowTeacher, self).get_context_data()
        context['is_pupils_teacher'] = self.request.user.pupil in self.object.pupils.all()
        return context


class ShowPupil(LoginRequiredMixin, UserIsTeacherMixin, DetailView):
    model = Pupil
    template_name = 'classes/show_pupil.html'

    def get_context_data(self, **kwargs):
        context = super(ShowPupil, self).get_context_data()
        if self.object in self.request.user.teacher.pupils.all():
            context['attempts'] = self.object.attempts.filter(mark__isnull=True)
        return context


class ShowProfile(LoginRequiredMixin, TemplateView):
    template_name = "classes/profile.html"

    def get_context_data(self, **kwargs):
        user_type = 'pupil'
        try:
            any_user = self.request.user.teacher
            if any_user is not None:
                user_type = 'teacher'
        except Teacher.DoesNotExist:
            if self.request.user.is_staff:
                user_type = 'admin'
        context = super(ShowProfile, self).get_context_data()
        if user_type is 'pupil':
            attempts = self.request.user.pupil.attempts.all()
            context['marked_attempts'] = attempts.filter(mark__isnull=False)
            context['teachers'] = self.request.user.pupil.teachers.all()
        if user_type is 'teacher':
            context['pupils'] = self.request.user.teacher.pupils.all()
        context['user_type'] = user_type
        return context


class TeachersList(ListView):
    model = Teacher
    template_name = 'classes/teachers_list.html'
