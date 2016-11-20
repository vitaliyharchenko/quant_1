from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tasks$', views.tasks_view, name="tasks_view"),
    url(r'^api/lesson_task/create$', views.lesson_task_create, name="lesson_task_create"),
]
