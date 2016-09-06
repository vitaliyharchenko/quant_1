# coding=utf-8
from django import template
from teaching.models import StudentGroupLesson

register = template.Library()


@register.assignment_tag
def studentgrouplesson(user, grouplesson):
    try:
        studentgrouplesson = StudentGroupLesson.objects.get(grouplesson=grouplesson, student=user)
    except StudentGroupLesson.DoesNotExist:
        studentgrouplesson = StudentGroupLesson.objects.create(grouplesson=grouplesson, student=user)
    return studentgrouplesson