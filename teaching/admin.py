from django.contrib import admin
from .models import ChoiceQuestion, ChoiceQuestionOption, BlockResult, ChoiceQuestionResult, Test, TestResult, \
    Group, StudentGroup, Lesson, GroupLesson, TextBlock, Subject, Task, StudentGroupLesson


class ChoiceQuestionOptionInline(admin.StackedInline):
    model = ChoiceQuestionOption
    extra = 2


class ChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceQuestionOptionInline]

# Register your models here.
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(BlockResult)
admin.site.register(ChoiceQuestionResult)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Group)
admin.site.register(StudentGroup)
admin.site.register(StudentGroupLesson)
admin.site.register(Lesson)
admin.site.register(GroupLesson)
admin.site.register(TextBlock)
admin.site.register(Subject)
admin.site.register(Task)
