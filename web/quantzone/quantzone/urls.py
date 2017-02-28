"""physicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import blocks.urls
import courses.urls
import lms.urls
import nodes.urls
import pages.urls
import tasks.urls
import testing.urls
import users.urls
from quantzone import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^markdown/', include('django_markdown.urls')),
]

urlpatterns += blocks.urls.urlpatterns
urlpatterns += courses.urls.urlpatterns
urlpatterns += users.urls.urlpatterns
urlpatterns += lms.urls.urlpatterns
urlpatterns += nodes.urls.urlpatterns
urlpatterns += pages.urls.urlpatterns
urlpatterns += tasks.urls.urlpatterns
urlpatterns += testing.urls.urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
