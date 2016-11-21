from django.db import models
from blocks.models import LessonBlockRelation
from users.models import User


# Nodes - nodes of learning graph
# objects with nodes class are:
#   -> Subject
#       -> Module
#           -> Unit
#               -> Lesson
class Node(models.Model):
    class Meta:
        verbose_name = 'Узел'
        verbose_name_plural = 'Узлы'

    title = models.CharField('Название объекта', max_length=300)

    def __str__(self):
        return self.title


class Subject(Node):
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    image = models.ImageField('Картинка', upload_to='subjects/', null=True, blank=True)

    @property
    def subject_modules(self):
        return SubjectModuleRelation.objects.filter(parent=self).order_by('order')


class Module(Node):
    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    @property
    def module_units(self):
        return ModuleUnitRelation.objects.filter(parent=self).order_by('order')


class Unit(Node):
    class Meta:
        verbose_name = 'Подраздел модуля'
        verbose_name_plural = 'Подразделы модулей'

    @property
    def unit_lessons(self):
        return UnitLessonRelation.objects.filter(parent=self).order_by('order')


class Lesson(Node):
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    about = models.TextField('Описание урока')

    def get_absolute_url(self):
        return "/lesson/%i" % self.id

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
    class Meta:
        verbose_name = 'Связь между узлами'
        verbose_name_plural = 'Связи между узлами'

    parent = models.ForeignKey(Node, verbose_name=u'Parent', related_name=u'parent_in_node_relation')
    child = models.ForeignKey(Node, verbose_name=u'Child', related_name=u'child_in_node_relation')


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
