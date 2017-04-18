from django.conf.urls import url

from . import views
from .autocomplete import NodeAutocomplete

urlpatterns = [
    url(r'^graph$', views.graph_view, name='graph'),
    url(r'^svg_graph$', views.svg_view, name='svg_view'),

    url(r'^create_node$', views.create_node, name='create_node'),
    url(r'^create_edge$', views.create_edge, name='create_edge'),

    url(r'^node-autocomplete/$', NodeAutocomplete.as_view(), name='node-autocomplete'),
]
