# coding=utf-8
from django import template
from lms.models import StudentModuleRelation

register = template.Library()


@register.assignment_tag
def student_module(user, module):
    try:
        student_module = StudentModuleRelation.objects.get(module=module, student=user)
    except StudentModuleRelation.DoesNotExist:
        student_module = StudentModuleRelation.objects.create(module=module, student=user)
    return student_module
