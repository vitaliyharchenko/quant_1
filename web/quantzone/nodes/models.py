from django.core.urlresolvers import reverse
from django.db import models

from blocks.models import LessonBlockRelation


# Nodes - nodes of learning graph
# objects with nodes class are:
#   -> Subject
#       -> Module
#           -> Unit
#               -> Lesson
class SubjectTag(models.Model):
    title = models.CharField('Название объекта', max_length=300)

    def __str__(self):
        return self.title


class Node(models.Model):
    title = models.CharField('Название объекта', max_length=300)
    subject_tag = models.ForeignKey(SubjectTag)

    class Meta:
        verbose_name = 'Узел'
        verbose_name_plural = 'Узлы'

    def __str__(self):
        return self.title


class Subject(Node):
    image = models.ImageField('Картинка', upload_to='subjects/', null=True, blank=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    @property
    def subject_modules(self):
        return SubjectModuleRelation.objects.filter(parent=self)


class Module(Node):
    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    @property
    def module_unit_relations(self):
        return ModuleUnitRelation.objects.filter(parent=self)


class Unit(Node):
    class Meta:
        verbose_name = 'Подраздел модуля'
        verbose_name_plural = 'Подразделы модулей'

    @property
    def unit_lesson_relations(self):
        return UnitLessonRelation.objects.filter(parent=self)


class Lesson(Node):
    about = models.TextField('Описание урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def get_absolute_url(self):
        return reverse('lesson_view', args=[self.id])

    @property
    def lesson_block_relations(self):
        lesson_block_relations = LessonBlockRelation.objects.filter(lesson=self)
        return lesson_block_relations


# Relation objects between nodes
# NodeRelation
#   -> SubjectModuleRelation
#       -> ModuleUnitRelation
#           -> UnitLessonRelation
class NodeRelation(models.Model):
    parent = models.ForeignKey(Node, verbose_name=u'Parent', related_name=u'parent_in_node_relation')
    child = models.ForeignKey(Node, verbose_name=u'Child', related_name=u'child_in_node_relation')

    class Meta:
        verbose_name = 'Связь между узлами'
        verbose_name_plural = 'Связи между узлами'

    def __str__(self):
        return "{} in {}".format(self.child, self.parent)


class SubjectModuleRelation(NodeRelation):
    class Meta:
        verbose_name = 'Связь между Subject и Module'
        verbose_name_plural = 'Связи между Subject и Module'


class ModuleUnitRelation(NodeRelation):
    class Meta:
        verbose_name = 'Связь между Module и Unit'
        verbose_name_plural = 'Связи между Module и Unit'


class UnitLessonRelation(NodeRelation):
    class Meta:
        verbose_name = 'Связь между Unit и Lesson'
        verbose_name_plural = 'Связи между Unit и Lesson'
