from django.db import models

from markdownx.models import MarkdownxField
from model_utils.managers import InheritanceManager


# All lessons contains blocks (text, choice, question with float answer)
class Block(models.Model):
    objects = InheritanceManager()


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
