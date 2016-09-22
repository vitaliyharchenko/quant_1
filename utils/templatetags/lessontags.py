# coding=utf-8
from django import template
from teaching.models import StudentGroupLesson, StudentLesson, CourseModule, StudentModule

register = template.Library()


@register.assignment_tag
def studentgrouplesson(user, grouplesson):
    try:
        studentgrouplesson = StudentGroupLesson.objects.get(grouplesson=grouplesson, student=user)
    except StudentGroupLesson.DoesNotExist:
        studentgrouplesson = StudentGroupLesson.objects.create(grouplesson=grouplesson, student=user)
    return studentgrouplesson


@register.assignment_tag
def studentmodule(user, module):
    try:
        studentmodule = StudentModule.objects.get(module=module, student=user)
    except StudentModule.DoesNotExist:
        studentmodule = StudentModule.objects.create(module=module, student=user)
    return studentmodule