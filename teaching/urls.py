from django.conf.urls import url, patterns
from . import views

urlpatterns = [
    url(r'^block/(?P<block_id>\d+)$', views.block_view, name="block_view"),
    url(r'^test/(?P<test_id>\d+)$', views.test_view, name="test_view"),
    url(r'^test/(?P<test_id>\d+)/(?P<block_num>\d+)$', views.test_block_view, name="test_block_view"),
    url(r'^test/(?P<test_id>\d+)/final$', views.test_final_view, name="test_final_view"),
    url(r'^test/results$', views.test_results_view, name="test_results_view"),

    url(r'^groups$', views.groups_view, name="groups_view"),
    url(r'^group/(?P<group_id>\d+)$', views.group_view, name="group_view"),
    url(r'^group/(?P<group_id>\d+)/lesson/(?P<lesson_id>\d+)$', views.grouplesson_view, name="grouplesson_view"),
]