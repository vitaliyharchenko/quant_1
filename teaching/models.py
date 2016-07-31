from django.db import models
from django.utils import timezone
from users.models import User


# Блоки, из которых строится занятие (контент, тест, опрос итд)
class Block(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.title


class Test(Block):
    class Meta():
        verbose_name = 'тестовый вопрос'
        verbose_name_plural = 'тестовые вопросы'

    question_text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class TestOption(models.Model):
    class Meta():
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    test = models.ForeignKey(Test)
    option_text = models.CharField(max_length=300)
    is_true = models.BooleanField()


# class TestResult(models.Model):
#     user = models.ForeignKey(User)
#     test = models.ForeignKey(Test)
#     date = models.DateField(default=timezone.now)
#     score = models.IntegerField(null=True, blank=True)
#     max_score = models.IntegerField()