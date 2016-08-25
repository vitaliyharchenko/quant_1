import markdown
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django_markdown.models import MarkdownField
from pyembed.markdown import PyEmbedMarkdown
from users.models import User


class Subject(models.Model):
    class Meta():
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    title = models.TextField()

    def __str__(self):
        return self.title


# учебный день
class Lesson(models.Model):
    class Meta():
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    title = models.CharField('Название урока', max_length=300)
    has_homework = models.BooleanField('Есть домашка?')
    blocks = ArrayField(models.IntegerField())

    def __str__(self):
        return self.title


# Связь ученика с уроком
# Будет глобально везде, даже для заочников
# class StudentLesson(models.Model):
#     class Meta():
#         verbose_name = 'Связь ученика с уроком'
#
#     lesson = models.ForeignKey(Lesson)
#     student = models.ForeignKey(User)
#     is_finished = models.BooleanField('Закончил?')
#     has_perm = models.BooleanField('Имеет право начать?')
#     score = models.IntegerField(null=True, blank=True)
#     max_score = models.IntegerField(null=True, blank=True)


# ==============
# УЧЕБНЫЕ ГРУППЫ
# ==============
class Group(models.Model):
    class Meta():
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    title = models.CharField('Название группы', max_length=300)
    teacher = models.ForeignKey(User)
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.title

    @property
    def studentgroups(self):
        return StudentGroup.objects.filter(group=self)

    @property
    def grouplessons(self):
        return GroupLesson.objects.filter(group=self).order_by('datetime')


# Привязка студента к группе для очных групп
class StudentGroup(models.Model):
    class Meta():
        verbose_name = 'Участие студента в группе'
        verbose_name_plural = 'Участие студента в группе'
        unique_together = ('group', 'student')

    group = models.ForeignKey(Group)
    student = models.ForeignKey(User)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.group.title)


# Связь группы с уроками, с указанием порядкового номера урока
# Только для очных занятий
class GroupLesson(models.Model):
    class Meta():
        verbose_name = 'Порядковое включение урока в группу'
        unique_together = ('group', 'lesson')

    lesson = models.ForeignKey(Lesson)
    group = models.ForeignKey(Group)
    datetime = models.DateTimeField(null=True, blank=True)
    datetime_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u'{} in "{}"'.format(self.lesson, self.group.title)

    @property
    def time_status(self):
        now = timezone.localtime(timezone.now())
        if now <= self.datetime:
            return 'WILL BE'
        elif now <= self.datetime:
            return 'NOW'
        else:
            return 'WAS'

    @property
    def is_next(self):
        query = GroupLesson.objects.filter(group=self.group).filter(datetime_to__gt=timezone.now()).order_by('datetime')
        if query and query[0] == self:
            return True
        else:
            return False


# Связь ученика с уроком d группе. Позволяет ставить оценки за конкретное занятие в конкретный день
# только ради очных занятий в Юниуме
class StudentGroupLesson(models.Model):
    class Meta():
        verbose_name = 'Связь ученика с уроком в группе'
        unique_together = ('grouplesson', 'student')

    grouplesson = models.ForeignKey(GroupLesson)
    student = models.ForeignKey(User)

    teacher_score = models.IntegerField(null=True, blank=True)
    own_score = models.IntegerField(null=True, blank=True)

    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)

    has_perm = models.BooleanField('Имеет право начать?', default=False)
    is_finished = models.BooleanField('Закончил домашку?', default=False)
    is_visited = models.BooleanField('Посетил занятие?', default=False)


# домашнее задание
class Task(models.Model):
    class Meta():
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    student = models.ForeignKey(User)
    datetime = models.DateTimeField(null=True, blank=True)
    datetime_to = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField('Закончил?', default=False)


class GroupLessonTask(Task):
    class Meta():
        verbose_name = 'Домашнее задание в группе'
        verbose_name_plural = 'Домашние задания в группе'

    grouplesson = models.ForeignKey(GroupLesson)

    def __str__(self):
        return u'For {}, "{}"'.format(self.student, self.grouplesson.lesson)


# Блоки, из которых строится занятие (контент, тест, опрос итд)
class Block(models.Model):
    def __str__(self):
        return u'Block #{}'.format(self.id)


class TextBlock(Block):
    class Meta():
        verbose_name = 'текстовая статья'
        verbose_name_plural = 'текстовые статьи'

    title = models.CharField(max_length=200, unique=True)
    body = MarkdownField()

    def __str__(self):
        return self.title

    @property
    def rendered_content(self):
        return markdown.markdown(self.body, extensions=['markdown.extensions.extra', PyEmbedMarkdown(), 'mdx_math'])


class ChoiceQuestion(Block):
    class Meta():
        verbose_name = 'тестовый вопрос'
        verbose_name_plural = 'тестовые вопросы'

    question_text = models.CharField('Текст вопроса', max_length=200)

    def __str__(self):
        return self.question_text


class ChoiceQuestionOption(models.Model):
    class Meta():
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    choicequestion = models.ForeignKey(ChoiceQuestion)
    option_text = models.CharField('Вариант ответа', max_length=300)
    help_text = models.CharField('Подсказка', max_length=300, blank=True)
    is_true = models.BooleanField('Правильный?')

    def __str__(self):
        return self.option_text


class BlockResult(models.Model):
    class Meta():
        verbose_name = 'Результат ответа'
        verbose_name_plural = 'Результаты ответов'

    user = models.ForeignKey(User)
    block = models.ForeignKey(Block)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()

    def __str__(self):
        return u'{}, {}, {}'.format(self.user, self.block, self.date)


class ChoiceQuestionResult(BlockResult):
    class Meta():
        verbose_name = 'Результат ответа на тестовый вопрос'
        verbose_name_plural = 'Результаты ответов на тестовые вопросы'

    choices = ArrayField(models.IntegerField())


class Test(models.Model):
    class Meta():
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return u'Test #{}'.format(self.id)

    blocks = ArrayField(models.IntegerField())
    about = models.CharField('Описание теста', max_length=400)


class TestResult(models.Model):
    class Meta():
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True)
    results = models.ManyToManyField(BlockResult, blank=True)

    def __str__(self):
        return u'{}, {}, {}'.format(self.user, self.test, self.date)