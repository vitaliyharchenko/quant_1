from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile$', views.profile_view, name='profile'),
]
