from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^new/$', views.CreateTask.as_view(), name='create_task'),
    url(r'^new_category/$', views.CreateCategory.as_view(), name='create_category'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^answer_task/(?P<pk>[0-9]+)/$', views.BindPupilToTeacher.as_view(), name='bind_to_teacher'),
]
