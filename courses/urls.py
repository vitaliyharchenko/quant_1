from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^courses$', views.courses_view, name="courses_view"),
    url(r'^course/(?P<course_id>\d+)$', views.course_view, name="course_view"),
]
