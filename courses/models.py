from django.db import models
from nodes.models import Subject
from users.models import User
from lms.models import StudentCourse
from nodes.models import Module


# Create your models here.
class Course(models.Model):
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    title = models.CharField('Название курса', max_length=300)
    subject = models.ForeignKey(Subject)
    owner = models.ForeignKey(User)
    about = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/course/%i" % self.id

    @property
    def student_courses(self):
        student_courses = StudentCourse.objects.filter(course=self)
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

