from django.conf.urls import url, include
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^teacher_connect/(?P<pk>[0-9]+)/$', views.BindPupilToTeacher.as_view(), name='bind_to_teacher'),
]
