# coding=utf-8
from django import template
from lms.models import StudentModule

register = template.Library()


@register.assignment_tag
def student_module(user, module):
    try:
        student_module = StudentModule.objects.get(module=module, student=user)
    except StudentModule.DoesNotExist:
        student_module = StudentModule.objects.create(module=module, student=user)
    return student_module
