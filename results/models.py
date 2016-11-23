from django.utils import timezone
from django.db import models
from blocks.models import Block
from users.models import User
from nodes.models import Lesson
from testing.models import Test
from django.contrib.postgres.fields import ArrayField


class Result(models.Model):

    student = models.ForeignKey(User, verbose_name=u'Ученик')
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()


class LessonResult(Result):
    class Meta:
        verbose_name = 'Результат урока'
        verbose_name_plural = 'Результаты уроков'

    lesson = models.ForeignKey(Lesson, verbose_name=u'Урок')

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.lesson, self.date)

    @property
    def lesson_result_block_result_relations(self):
        return LessonResultBlockResultRelation.objects.filter(lesson_result=self)


class TestResult(Result):
    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    test = models.ForeignKey(Test, verbose_name=u'Тест')

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.test, self.date)


# =================
# Results of blocks
# =================
class BlockResult(Result):
    class Meta:
        verbose_name = 'Результат ответа на блок'
        verbose_name_plural = 'Результаты ответов на блоки'

    block = models.ForeignKey(Block)

    def __str__(self):
        return u'{}, {}, {}'.format(self.student, self.block, self.date)


class ChoiceBlockResult(BlockResult):
    class Meta:
        verbose_name = 'Результат ответа на тестовый вопрос'
        verbose_name_plural = 'Результаты ответов на тестовые вопросы'

    choices = ArrayField(models.IntegerField())


class FloatBlockResult(BlockResult):
    class Meta:
        verbose_name = 'Результат ответа на задачу'
        verbose_name_plural = 'Результаты ответов на задачи'

    answer = models.FloatField('Ответ')


# ========================
# Relation between results
# ========================
class LessonResultBlockResultRelation(models.Model):
    class Meta:
        verbose_name = 'Связь результата урока с результатом блока'

    lesson_result = models.ForeignKey(LessonResult)
    block_result = models.ForeignKey(BlockResult)
