from django.conf.urls import url, include
from django.contrib.auth.views import logout, login
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login', login, name='login'),
    url(r'', include('django.contrib.auth.urls')),
    url(r'^teacher_connect/(?P<pk>[0-9]+)/$', views.BindPupilToTeacher.as_view(), name='bind_to_teacher'),
    url(r'^teacher/(?P<pk>[0-9]+)/$', views.ShowTeacher.as_view(), name='show_teacher'),
    url(r'^pupil/(?P<pk>[0-9]+)/$', views.ShowPupil.as_view(), name='show_pupil'),
    url(r'^profile/$', views.ShowProfile.as_view(), name='show_profile'),
    url(r'^teachers_list/', views.TeachersList.as_view(), name="teachers_list"),
]
