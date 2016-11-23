from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lesson/(?P<lesson_id>\d+)/(?P<block_num>\d+)$', views.lesson_block_view, name="lesson_block_view"),

    url(r'^block/(?P<block_id>\d+)$', views.block_view, name="block_view"),
]
