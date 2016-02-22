from forms import UserRegistrationForm
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
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
