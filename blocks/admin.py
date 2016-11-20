from django.contrib import admin
from .models import *


class ChoiceBlockOptionInline(admin.TabularInline):
    model = ChoiceBlockOption
    extra = 4


class ChoiceBlockAdmin(admin.ModelAdmin):
    inlines = [ChoiceBlockOptionInline]


# Register your models here.
admin.site.register(ChoiceBlock, ChoiceBlockAdmin)
admin.site.register(FloatBlock)
admin.site.register(BlockResult)
admin.site.register(ChoiceBlockResult)
admin.site.register(TextBlock)
admin.site.register(LessonBlockRelation)
