from django.contrib import admin

from .models import LessonTask, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(LessonTask)
