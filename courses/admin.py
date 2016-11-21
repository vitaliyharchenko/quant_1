from django.contrib import admin
from .models import Course, CourseModuleRelation, StudentCourseRelation


# Register your models here.
admin.site.register(Course)
admin.site.register(CourseModuleRelation)
admin.site.register(StudentCourseRelation)
