from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^new/$', views.CreateTask.as_view(), name='create_task'),
    url(r'^new_category/$', views.CreateCategory.as_view(), name='create_category'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^answer_task/(?P<pk>[0-9]+)/$', views.SolutionAttempt.as_view(), name='solution_attempt'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryTasks.as_view(), name='tasks_by_category'),
]
