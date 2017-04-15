from django.contrib import admin

from .models import Group, StudentGroupRelation

# Register your models here.
admin.site.register(Group)
admin.site.register(StudentGroupRelation)
