from django.db import models

from events.models import Seminar
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
    student = models.ForeignKey(User, verbose_name=u'Student')
    has_perm = models.BooleanField('Имеет доступ?', default=False)

    class Meta:
        verbose_name = 'Связь ученика с узлом'


class StudentModuleRelation(StudentNodeRelation):
    module = models.ForeignKey(Module)

    class Meta:
        verbose_name = 'Связь ученика с уроком'

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.module)


class StudentLessonRelation(StudentNodeRelation):
    lesson = models.ForeignKey(Lesson)

    class Meta:
        verbose_name = 'Связь ученика с уроком'

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.lesson)


# Relation between student and seminar
class StudentSeminarRelation(models.Model):
    seminar = models.ForeignKey(Seminar, verbose_name=u"Семинар")
    student = models.ForeignKey(User, verbose_name=u'Студент')
    had_visit = models.BooleanField('Посетил?', default=False)

    class Meta:
        verbose_name = 'Связь ученика с семинаром'

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.seminar)


# Relation between student and course
class StudentCourseRelation(models.Model):
    course = models.ForeignKey('courses.Course')
    student = models.ForeignKey(User, verbose_name=u'Student')
    has_perm = models.BooleanField('Имеет доступ?', default=False)

    class Meta:
        verbose_name = 'Связь ученика с курсом'

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.course)


# Relation between student and teacher
class StudentTeacherRelation(models.Model):
    student = models.ForeignKey(User, related_name=u'student')
    teacher = models.ForeignKey(User, related_name=u'teacher', limit_choices_to={'is_teacher': True})

    class Meta:
        verbose_name = 'Связь ученика с учителем'

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.teacher)

    def tasks(self):
        return LessonTask.objects.filter(student=self.student).order_by('datetime')
