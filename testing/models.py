from django.db import models
from blocks.models import Block
from users.models import User


class Test(models.Model):
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return u'Test #{}'.format(self.id)

    title = models.CharField('Название', max_length=400)
    about = models.TextField('Описание теста')

    @property
    def test_block_relations(self):
        return TestBlockRelation.objects.filter(test=self).order_by('order')


class TestBlockRelation(models.Model):
    class Meta:
        verbose_name = 'Включение блока в тест'
        verbose_name_plural = 'Включение блока в тест'

    def __str__(self):
        return u'Test #{}'.format(self.id)

    test = models.ForeignKey(Test)
    block = models.ForeignKey(Block)
    order = models.IntegerField('Порядковый номер')
