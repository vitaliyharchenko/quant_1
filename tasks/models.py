from django.db import models
from users.models import User
from nodes.models import Lesson, LessonResult


# Tasks
class Task(models.Model):
    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    student = models.ForeignKey(User, related_name='task_student')
    teacher = models.ForeignKey(User, related_name='task_teacher')
    datetime = models.DateTimeField(null=True, blank=True)
    datetime_to = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField('Закончил?', default=False)


class LessonTask(Task):
    class Meta:
        verbose_name = 'Домашнее задание, урок'
        verbose_name_plural = 'Домашние задания, уроки'

    lesson = models.ForeignKey(Lesson)
    lesson_result = models.ForeignKey(LessonResult, blank=True, null=True)

    def __str__(self):
        return u'For {}, "{}"'.format(self.student, self.lesson)

