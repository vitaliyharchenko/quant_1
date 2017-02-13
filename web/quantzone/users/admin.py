from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, UserActivation

# Register your models here.
admin.site.register(User)
admin.site.register(UserActivation)
admin.site.unregister(Group)
