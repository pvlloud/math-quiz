from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^new/$', views.CreateTask.as_view(), name='create_task'),
    url(r'^new_category/$', views.CreateCategory.as_view(), name='create_category'),
    url(r'^answer_task/(?P<pk>[0-9]+)/$', views.SolutionAttempt.as_view(), name='solution_attempt'),
    url(r'^category/(?P<pk>[0-9]+)/level/(?P<level>[0-5])$', views.CategoryLevelTasks.as_view(), name='tasks_by_category'),
    url(r'^task/(?P<pk>[0-9]+)', views.ShowTask.as_view(), name="show_task"),
    url(r'^mark_attempt/(?P<pk>[0-9]+)', views.MarkAttempt.as_view(), name="mark_attempt"),
    url(r'^attempt/(?P<pk>[0-9]+)', views.ShowAttempt.as_view(), name="show_attempt"),
    url(r'^category_list/$', views.CategoryList.as_view(), name="category_list"),
    url(r'^create_homework/(?P<pupil>[0-9]+)/$', views.CreateHomework.as_view(), name='create_homework'),
    url(r'^add_homework_task/(?P<pk>[0-9]+)/(?P<task>[0-9]+)/$', views.AddTaskToHomework.as_view(), name='add_task_to_homework'),
    url(r'^close_homework/(?P<pk>[0-9]+)/$', views.CloseHomework.as_view(), name='close_homework'),
    url(r'^homework/(?P<homework>[0-9]+)/$', views.ShowHomework.as_view(), name='show_homework'),
]
