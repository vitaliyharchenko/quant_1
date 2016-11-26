from django.db import models
from django.utils import timezone

from nodes.models import Lesson
from users.models import User


# ============
# LessonResult
# ============
class LessonResult(models.Model):
    class Meta:
        verbose_name = 'Результат урока'
        verbose_name_plural = 'Результаты уроков'

    student = models.ForeignKey(User, verbose_name=u'Ученик')
    lesson = models.ForeignKey(Lesson, verbose_name=u'Урок')
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.lesson, self.date)
