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

    @property
    def student_group_relations(self):
        return StudentGroupRelation.objects.filter(group=self)


# StudentGroupRelations
class StudentGroupRelation(models.Model):

    ACTIVE = 'AT'
    INACTIVE = 'NA'
    STATUS_CHOICES = (
        (ACTIVE, 'Активная'),
        (INACTIVE, 'Неактивная'),
    )

    group = models.ForeignKey(Group)
    student = models.ForeignKey(User)
    status = models.CharField(u'Активность', max_length=2, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = 'Связь ученика с группой'
        verbose_name_plural = 'Связь ученика с группами'

    def __str__(self):
        return '{} in {}'.format(self.student, self.group)
