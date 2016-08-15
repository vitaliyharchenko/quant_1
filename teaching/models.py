import markdown
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django_markdown.models import MarkdownField
from pyembed.markdown import PyEmbedMarkdown
from users.models import User


# учебный день
class Lesson(models.Model):
    class Meta():
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    title = models.CharField('Название урока', max_length=300)
    has_homework = models.BooleanField('Есть домашка?')

    def __str__(self):
        return self.title


# ==============
# УЧЕБНЫЕ ГРУППЫ
# ==============
class StudyGroup(models.Model):
    class Meta():
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    title = models.CharField('Название группы', max_length=300)
    teacher = models.ForeignKey(User)

    def __str__(self):
        return self.title

    @property
    def lessons(self):
        return Lesson.objects.filter()


# Привязка студента к группе
class StudentStudyGroup(models.Model):
    class Meta():
        verbose_name = 'Участие студента в группе'
        verbose_name_plural = 'Участие студента в группе'
        unique_together = ('group', 'student')

    group = models.ForeignKey(StudyGroup)
    student = models.ForeignKey(User)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.group.title)


# Связь группы с уроками, с указанием порядкового номера урока
class StudyGroupLesson(models.Model):
    class Meta():
        verbose_name = 'Порядковое включение урока в группу'

    lesson = models.ForeignKey(Lesson)
    studygroup = models.ForeignKey(StudyGroup)
    datetime = models.DateTimeField(null=True, blank=True)
    datetime_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u'{} in "{}"'.format(self.lesson, self.studygroup.title)

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
        query = StudyGroupLesson.objects.filter(studygroup=self.studygroup).filter(datetime_to__gt=timezone.now())
        if query and query[0] == self:
            return True
        else:
            return False


# Связь ученика с уроком в группе
class StudentStudyGroupLesson(models.Model):
    class Meta():
        verbose_name = 'Связь ученика с уроком в группе'

    studygrouplesson = models.ForeignKey(StudyGroupLesson)
    student = models.ForeignKey(User)
    is_finished = models.BooleanField('Закончил?')


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