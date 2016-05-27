from forms import UserRegistrationForm, PupilKeywordForm
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from models import Teacher, Pupil


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
        if form.cleaned_data['if_teacher_keyword'] == 'keyword':
            teacher = Teacher.objects.create(user=new_user)
        else:
            pupil = Pupil.objects.create(user=new_user)
        return super(RegisterView, self).form_valid(form)


class BindPupilToTeacher(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = reverse_lazy('classes:login')
    template_name = 'classes/pupil_to_teacher_keyword.html'
    form_class = PupilKeywordForm

    def test_func(self):
        try:
            ppl = self.request.user.pupil
            if ppl is not None:
                return True
        except Pupil.DoesNotExist:
            return False

    def form_valid(self, form):
        teacher = Teacher.objects.get(pk=self.kwargs["pk"])
        if form.cleaned_data['keyword'] == teacher.keyword:
            teacher.pupils.add(self.request.user.pupil)
        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong Keyword!')
            return self.form_invalid(form)
        return super(BindPupilToTeacher, self).form_valid(form)
