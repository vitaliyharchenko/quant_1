from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, UserActivation
from teaching.models import LessonTask



class LessonTaskInline(admin.TabularInline):
    model = LessonTask
    extra = 4


class UserAdmin(admin.ModelAdmin):
    inlines = [LessonTaskInline]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserActivation)
admin.site.unregister(Group)
