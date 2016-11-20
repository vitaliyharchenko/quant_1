from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lesson/(?P<lesson_id>\d+)$', views.lesson_view, name="lesson_view"),
    url(r'^lesson/(?P<lesson_id>\d+)/final$', views.lesson_final_view, name="lesson_final_view"),
]
