from django.db import models

from nodes.models import Subject
from users.models import User


# Create your models here.
class Group(models.Model):
    title = models.CharField('Название группы', max_length=300)
    teacher = models.ForeignKey(User, verbose_name=u'Учитель', limit_choices_to={'is_teacher': True})
    subject = models.ForeignKey(Subject, verbose_name=u"Предмет")

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return self.title


class StudentGroup(models.Model):
    class Meta:
        verbose_name = 'Участие студента в группе'
        verbose_name_plural = 'Участие студента в группе'
        unique_together = ('group', 'student')

    group = models.ForeignKey(Group)
    student = models.ForeignKey(User)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.group.title)
