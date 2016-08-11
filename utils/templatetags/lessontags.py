# coding=utf-8
from django import template
from teaching.models import StudentStudyGroupLesson

register = template.Library()


# находит объект подписи на игру для заданной игры и пользователя
@register.assignment_tag
def studentstudygrouplesson(user, studygrouplesson):
    try:
        studentstudygrouplesson = StudentStudyGroupLesson.objects.get(studygrouplesson=studygrouplesson, student=user)
    except StudentStudyGroupLesson.DoesNotExist:
        return None
    return studentstudygrouplesson