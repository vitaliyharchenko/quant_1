from django.contrib import admin
from .models import ChoiceQuestion, ChoiceQuestionOption, BlockResult, ChoiceQuestionResult, Test, TestResult, \
    StudyGroup, StudentStudyGroup, Lesson, StudyGroupLesson, StudentStudyGroupLesson, TextBlock


class ChoiceQuestionOptionInline(admin.StackedInline):
    model = ChoiceQuestionOption
    extra = 1


class ChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceQuestionOptionInline]

# Register your models here.
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(BlockResult)
admin.site.register(ChoiceQuestionResult)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(StudyGroup)
admin.site.register(StudentStudyGroup)
admin.site.register(Lesson)
admin.site.register(StudyGroupLesson)
admin.site.register(StudentStudyGroupLesson)
admin.site.register(TextBlock)