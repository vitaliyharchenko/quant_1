from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index_view'),

    url(r'^graph$', views.graph_view, name='graph_view'),
    url(r'^svg_graph$', views.svg_view, name='svg_view'),

    url(r'^landing/(?P<landing_id>\d+)$', views.landing_view, name='landing_view'),
]
