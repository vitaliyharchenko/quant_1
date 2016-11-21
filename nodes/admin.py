from django.contrib import admin
from nodes.models import *


admin.site.register(Node)

admin.site.register(Subject)
admin.site.register(Module)
admin.site.register(Unit)
admin.site.register(Lesson)

admin.site.register(SubjectModuleRelation)
admin.site.register(ModuleUnitRelation)
admin.site.register(UnitLessonRelation)
