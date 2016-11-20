from django.contrib import admin
from .models import Task, LessonTask


# Register your models here.
admin.site.register(Task)
admin.site.register(LessonTask)
