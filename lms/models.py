from django.db import models

from nodes.models import Lesson, Module
from tasks.models import LessonTask
from users.models import User


# Relation between student and node
# StudentNode
#   -> StudentSubject
#   -> StudentModule
#   -> StudentUnit
#   -> StudentLesson
class StudentNodeRelation(models.Model):
    class Meta:
        verbose_name = 'Связь ученика с узлом'

    student = models.ForeignKey(User, verbose_name=u'Student')
    has_perm = models.BooleanField('Имеет доступ?', default=False)


class StudentModuleRelation(StudentNodeRelation):
    class Meta:
        verbose_name = 'Связь ученика с уроком'

    module = models.ForeignKey(Module)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.module)


class StudentLessonRelation(StudentNodeRelation):
    class Meta:
        verbose_name = 'Связь ученика с уроком'

    lesson = models.ForeignKey(Lesson)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.lesson)


# Relation between student and course
class StudentCourseRelation(models.Model):
    class Meta:
        verbose_name = 'Связь ученика с курсом'

    course = models.ForeignKey('courses.Course')
    student = models.ForeignKey(User, verbose_name=u'Student')
    has_perm = models.BooleanField('Имеет доступ?', default=False)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.course)


# Relation between student and teacher
class StudentTeacherRelation(models.Model):
    class Meta:
        verbose_name = 'Связь ученика с учителем'

    student = models.ForeignKey(User, related_name=u'student')
    teacher = models.ForeignKey(User, related_name=u'teacher')

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.teacher)

    def tasks(self):
        return LessonTask.objects.filter(student=self.student).order_by('datetime')
