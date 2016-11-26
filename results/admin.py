from django.contrib import admin

from .models import *

admin.site.register(LessonResult)
admin.site.register(TestResult)
admin.site.register(BlockResult)
admin.site.register(ChoiceBlockResult)
admin.site.register(LessonResultBlockResultRelation)
