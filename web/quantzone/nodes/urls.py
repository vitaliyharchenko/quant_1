from django.conf.urls import url

from . import views
from .autocomplete import NodeAutocomplete

urlpatterns = [
    url(r'^graph$', views.graph_view, name='graph'),
    url(r'^svg_graph$', views.svg_view, name='svg_view'),

    url(r'^node-autocomplete/$', NodeAutocomplete.as_view(), name='node-autocomplete'),
]
