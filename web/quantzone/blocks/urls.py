from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^blocks/(?P<block_id>[0-9]+)$', views.block, name='block'),
]
