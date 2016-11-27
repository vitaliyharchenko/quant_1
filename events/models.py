from django.db import models

from places.models import СlassRoom
from users.models import User


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    created_by = models.ForeignKey(User, blank=True, null=True)
    datetime = models.DateTimeField(verbose_name='Дата и время начала')
    datetime_to = models.DateTimeField(verbose_name='Дата и время окончания', blank=True)
    cost = models.DecimalField(verbose_name=u"Стоимость посещения", decimal_places=8, max_digits=8)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'


class Seminar(Event):
    teacher = models.ForeignKey(User, verbose_name=u"Учитель", limit_choices_to={'is_teacher': True})
    class_room = models.ForeignKey(СlassRoom, verbose_name=u"Аулитория")

    class Meta:
        verbose_name = 'семинар'
        verbose_name_plural = 'семинар'
