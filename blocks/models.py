from django.db import models
from django.utils import timezone
from django_markdown.models import MarkdownField

from users.models import User


# All lessons contains blocks (text, chioce, question with float answer)
class Block(models.Model):

    def __str__(self):
        title = None

        try:
            title = self.textblock.title
        except AttributeError:
            pass

        try:
            title = self.choiceblock.question_text[:100]
        except AttributeError:
            pass

        try:
            title = self.floatquestion.question_text[:100]
        except AttributeError:
            pass

        if title:
            return title
        else:
            return u'Block #{}'.format(self.id)

    def get_absolute_url(self):
        return "/block/%i" % self.id


class TextBlock(Block):
    title = models.CharField(max_length=200, unique=True)
    body = MarkdownField()

    class Meta:
        verbose_name = 'текстовая статья'
        verbose_name_plural = 'текстовые статьи'

    def __str__(self):
        return self.title


class ChoiceBlock(Block):
    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='choice_blocks/', null=True, blank=True)

    class Meta:
        verbose_name = 'тестовый вопрос'
        verbose_name_plural = 'тестовые вопросы'

    def __str__(self):
        return self.question_text


class ChoiceBlockOption(models.Model):
    choice_block = models.ForeignKey(ChoiceBlock)
    option_text = models.CharField('Вариант ответа', max_length=600, blank=True)
    option_image = models.ImageField('Картинка', upload_to='choice_block_options/', null=True, blank=True)
    help_text = models.CharField('Подсказка', max_length=300, blank=True)
    is_true = models.BooleanField('Правильный?')

    class Meta:
        verbose_name = 'Вариант ответа на тестовый вопрос'
        verbose_name_plural = 'Варианты ответа на тестовые вопросы'

    def __str__(self):
        return self.option_text


class FloatBlock(Block):
    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='float_questions/', null=True, blank=True)
    answer = models.FloatField('Ответ')

    class Meta:
        verbose_name = 'задача с численным ответом'
        verbose_name_plural = 'задачи с численным ответом'

    def __str__(self):
        return self.question_text


# Включение блоков в урок
class LessonBlockRelation(models.Model):
    lesson = models.ForeignKey('nodes.Lesson')
    block = models.ForeignKey(Block)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'включение блока в урок'
        verbose_name_plural = 'включения блоков в урок'
