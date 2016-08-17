# coding=utf-8
from django import template
from teaching.models import StudentLesson

register = template.Library()


@register.assignment_tag
def studentlesson(user, lesson):
    try:
        studentlesson = StudentLesson.objects.get(lesson=lesson, student=user)
    except StudentLesson.DoesNotExist:
        return None
    return studentlesson