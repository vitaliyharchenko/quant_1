from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(StudentLessonRelation)
admin.site.register(StudentNodeRelation)
admin.site.register(StudentTeacherRelation)
admin.site.register(StudentSeminarRelation)
