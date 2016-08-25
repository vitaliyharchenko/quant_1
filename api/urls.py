from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/studentgrouplesson/action$', views.studentgrouplesson_action, name="studentgrouplesson_action"),
]