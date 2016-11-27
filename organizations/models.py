from django.db import models

from users.models import User


class Company(models.Model):
    title = models.CharField(verbose_name=u'Организация', max_length=200, unique=True)

    class Meta:
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return self.title


class CompanyTeacherRelation(models.Model):
    company = models.ForeignKey(Company, verbose_name=u'Компания')
    teacher = models.ForeignKey(User, verbose_name=u'Учитель', limit_choices_to={'is_teacher': True})

    class Meta:
        verbose_name = 'связь учителя с компанией'

    def __str__(self):
        return "{} in {}".format(self.teacher, self.organization)


class CompanyStudentRelation(models.Model):
    company = models.ForeignKey(Company, verbose_name=u'Компания')
    student = models.ForeignKey(User, verbose_name=u'Студент')

    class Meta:
        verbose_name = 'связь ученика с компанией'

    def __str__(self):
        return "{} in {}".format(self.student, self.organization)
