from django.contrib import admin

from .models import (StudentLessonRelation, StudentNodeRelation,
                     StudentTeacherRelation)

# Register your models here.
admin.site.register(StudentLessonRelation)
admin.site.register(StudentNodeRelation)
admin.site.register(StudentTeacherRelation)
