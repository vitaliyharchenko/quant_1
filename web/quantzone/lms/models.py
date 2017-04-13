from django.db import models

from users.models import User


# Learning group
class Group(models.Model):
    title = models.CharField('Название группы', max_length=300)
    owner = models.ForeignKey(User)
    about = models.TextField()

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return None
