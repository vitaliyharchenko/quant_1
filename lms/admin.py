from django.contrib import admin
from .models import StudentLesson, StudentNode, StudentTeacher


# Register your models here.
admin.site.register(StudentLesson)
admin.site.register(StudentNode)
admin.site.register(StudentTeacher)
