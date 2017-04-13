from django.db import models


# Pointer on subject (math, physics and etc)
class SubjectTag(models.Model):
    title = models.CharField('Название объекта', max_length=300)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


# Nodes - particles of education path
class Node(models.Model):

    DEFINITION = 1
    METHOD = 2
    CHOICES = (
        (DEFINITION, 'Понятие'),
        (METHOD, 'Метод')
    )

    title = models.CharField('Название объекта', max_length=300)
    subject_tag = models.ForeignKey(SubjectTag)
    type_tag = models.PositiveSmallIntegerField(choices=CHOICES)

    class Meta:
        verbose_name = 'Узел'
        verbose_name_plural = 'Узлы'

    def __str__(self):
        return self.title


# TODO: add autocomplete on admin
# Relation between nodes. Directed graph structure
class NodeRelation(models.Model):
    parent = models.ForeignKey(Node, verbose_name=u'Parent', related_name=u'parent_in_node_relation')
    child = models.ForeignKey(Node, verbose_name=u'Child', related_name=u'child_in_node_relation')

    class Meta:
        verbose_name = 'Связь между узлами'
        verbose_name_plural = 'Связи между узлами'

    def __str__(self):
        return "{} in {}".format(self.child, self.parent)
