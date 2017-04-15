from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^groups$', views.groups, name='groups'),

    url(r'^group/(?P<group_id>\d+)$', views.group, name='group'),
]
