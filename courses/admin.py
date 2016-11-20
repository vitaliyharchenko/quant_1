from django.contrib import admin
from .models import Course, CourseModuleRelation, StudentCourse


# Register your models here.
admin.site.register(Course)
admin.site.register(CourseModuleRelation)
admin.site.register(StudentCourse)
