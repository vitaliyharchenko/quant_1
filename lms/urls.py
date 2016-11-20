from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^cabinet$', views.cabinet_view, name="cabinet_view"),
]
