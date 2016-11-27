from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test/(?P<test_id>\d+)$', views.test_view, name="test_view"),
    url(r'^test/(?P<test_id>\d+)/(?P<block_num>\d+)$', views.test_block_view, name="test_block_view"),
    url(r'^test/(?P<test_id>\d+)/final$', views.test_final_view, name="test_final_view"),
]
