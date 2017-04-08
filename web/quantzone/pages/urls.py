from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^styleguide$', views.styleguide, name='styleguide'),
    url(r'^email_styleguide$', views.email_styleguide, name='email_styleguide'),
]
