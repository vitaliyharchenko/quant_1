from django.db import models
from django.shortcuts import reverse

from markdownx.models import MarkdownxField
from model_utils.managers import InheritanceManager


# All lessons contains blocks (text, choice, question with float answer)
class Block(models.Model):
    objects = InheritanceManager()

    def get_absolute_url(self):
        return reverse('blocks:block', args=[str(self.id)])

    def class_name(self):
        return self.__class__.__name__


class TextBlock(Block):
    title = MarkdownxField()
    # TODO: add custom view for creating lectures
    body = MarkdownxField()

    class Meta:
        verbose_name = 'текстовая статья'
        verbose_name_plural = 'текстовые статьи'

    def __str__(self):
        return self.title


class ChoiceBlock(Block):
    question_text = MarkdownxField()
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
    is_true = models.BooleanField('Правильный?')

    class Meta:
        verbose_name = 'Вариант ответа на тестовый вопрос'
        verbose_name_plural = 'Варианты ответа на тестовые вопросы'

    def __str__(self):
        return self.option_text
