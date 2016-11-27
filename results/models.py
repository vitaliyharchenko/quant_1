from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from blocks.models import Block
from nodes.models import Lesson
from testing.models import Test
from users.models import User


class Result(models.Model):
    student = models.ForeignKey(User, verbose_name=u'Ученик')
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


class LessonResult(Result):
    lesson = models.ForeignKey(Lesson, verbose_name=u'Урок')

    class Meta:
        verbose_name = 'Результат урока'
        verbose_name_plural = 'Результаты уроков'

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.lesson, self.date)

    @property
    def lesson_result_block_result_relations(self):
        return LessonResultBlockResultRelation.objects.filter(lesson_result=self)


class TestResult(Result):
    test = models.ForeignKey(Test, verbose_name=u'Тест')

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.test, self.date)


# =================
# Results of blocks
# =================
class BlockResult(Result):
    block = models.ForeignKey(Block)

    class Meta:
        verbose_name = 'Результат ответа на блок'
        verbose_name_plural = 'Результаты ответов на блоки'

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.block, self.date)


class ChoiceBlockResult(BlockResult):
    choices = ArrayField(models.IntegerField())

    class Meta:
        verbose_name = 'Результат ответа на тестовый вопрос'
        verbose_name_plural = 'Результаты ответов на тестовые вопросы'


class FloatBlockResult(BlockResult):
    answer = models.FloatField('Ответ')

    class Meta:
        verbose_name = 'Результат ответа на задачу'
        verbose_name_plural = 'Результаты ответов на задачи'


# ========================
# Relation between results
# ========================
class LessonResultBlockResultRelation(models.Model):
    lesson_result = models.ForeignKey(LessonResult)
    block_result = models.ForeignKey(BlockResult)

    class Meta:
        verbose_name = 'Связь результата урока с результатом блока'
