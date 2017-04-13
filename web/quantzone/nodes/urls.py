from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^graph$', views.graph_view, name='graph'),
    url(r'^svg_graph$', views.svg_view, name='svg_view'),
]
