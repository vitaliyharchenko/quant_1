from django.contrib import admin

from .models import ChoiceQuestion, ChoiceQuestionOption, BlockResult, ChoiceQuestionResult, Test, TestResult, \
    Group, StudentGroup, Lesson, GroupLesson, TextBlock, Subject, Task, StudentGroupLesson, FloatQuestion, Course, \
    StudentCourse, ModuleLesson, StudentLesson, LessonBlock, Module, CourseModule


class ChoiceQuestionOptionInline(admin.TabularInline):
    model = ChoiceQuestionOption
    extra = 4


class ChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceQuestionOptionInline]


class CourseModulesInline(admin.TabularInline):
    model = CourseModule
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseModulesInline]


class ModuleLessonInline(admin.TabularInline):
    model = ModuleLesson
    extra = 1


class ModuleAdmin(admin.ModelAdmin):
    inlines = [ModuleLessonInline]


class LessonBlockInline(admin.TabularInline):
    model = LessonBlock
    extra = 1


class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonBlockInline]


# Register your models here.
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(FloatQuestion)
admin.site.register(BlockResult)
admin.site.register(ChoiceQuestionResult)
admin.site.register(Test)
admin.site.register(TestResult)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentLesson)

admin.site.register(Course, CourseAdmin)
admin.site.register(StudentCourse)

admin.site.register(Module, ModuleAdmin)

admin.site.register(Group)
admin.site.register(StudentGroup)
admin.site.register(StudentGroupLesson)
admin.site.register(GroupLesson)

admin.site.register(TextBlock)
admin.site.register(Subject)
admin.site.register(Task)
