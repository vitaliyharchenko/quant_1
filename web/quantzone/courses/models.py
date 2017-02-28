from django.db import models
from django.shortcuts import reverse
from lms.models import StudentCourseRelation
from nodes.models import Module, Subject

from users.models import User


# Create your models here.
class Course(models.Model):
    title = models.CharField('Название курса', max_length=300)
    subject = models.ForeignKey(Subject)
    owner = models.ForeignKey(User)
    about = models.TextField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_view', args=[self.id])

    @property
    def student_courses(self):
        student_courses = StudentCourseRelation.objects.filter(course=self)
        return student_courses

    @property
    def course_module_relations(self):
        return CourseModuleRelation.objects.filter(course=self).order_by('order')


class CourseModuleRelation(models.Model):
    class Meta:
        verbose_name = 'Порядковое включение модулей в курс'
        unique_together = ('course', 'module')

    course = models.ForeignKey(Course)
    module = models.ForeignKey(Module)
    order = models.IntegerField()

    def __str__(self):
        return "{} in {}".format(self.module, self.course)
