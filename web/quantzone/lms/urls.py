from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^groups$', views.groups, name='groups'),

    url(r'^group/(?P<group_id>\d+)$', views.group, name='group'),
    url(r'^group/(?P<group_id>\d+)/change$', views.student_group_change, name='student_group_change'),

    url(r'^group1/(?P<group_id>\d+)$', views.test_group, name='group1'),
]
