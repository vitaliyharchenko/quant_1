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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/lesson/%i" % self.id

    @property
    def lessonblocks(self):
        lessonblocks = LessonBlock.objects.filter(lesson=self)
        return lessonblocks


# Связь ученика с уроком
# Будет глобально везде, даже для заочников
class StudentLesson(models.Model):
    class Meta():
        verbose_name = 'Связь ученика с уроком'

    lesson = models.ForeignKey(Lesson)
    student = models.ForeignKey(User)
    is_finished = models.BooleanField('Закончил?', default=False)
    has_perm = models.BooleanField('Имеет право начать?', default=False)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return u'{} in "{}"'.format(self.student, self.lesson)


# ==============
# УЧЕБНЫЕ КУРСЫ
# ==============
class Course(models.Model):
    class Meta():
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    title = models.CharField('Название курса', max_length=300)
    subject = models.ForeignKey(Subject)
    owner = models.ForeignKey(User)
    about = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/course/%i" % self.id

    @property
    def studentcourses(self):
        studentcourses = StudentCourse.objects.filter(course=self)
        return studentcourses

    @property
    def coursemodules(self):
        return CourseModule.objects.filter(course=self).order_by('order')


# Привязка студента к курсу
class StudentCourse(models.Model):
    class Meta():
        verbose_name = 'Участие студента в курсе'
        verbose_name_plural = 'Участие студента в курсе'
        unique_together = ('course', 'student')

    course = models.ForeignKey(Course)
    student = models.ForeignKey(User)


class Module(models.Model):
    class Meta():
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    title = models.CharField('Название модуля', max_length=300)

    def __str__(self):
        return self.title

    @property
    def modulelessons(self):
        return ModuleLesson.objects.filter(module=self).order_by('order')


class CourseModule(models.Model):
    class Meta():
        verbose_name = 'Порядковое включение модулей в курс'
        unique_together = ('course', 'module')

    course = models.ForeignKey(Course)
    module = models.ForeignKey(Module)
    order = models.IntegerField()


# Связь ученика с модулем.
class StudentModule(models.Model):
    class Meta():
        verbose_name = 'Связь ученика с модулем'
        unique_together = ('module', 'student')

    module = models.ForeignKey(Module)
    student = models.ForeignKey(User)

    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(null=True, blank=True)

    has_perm = models.BooleanField('Имеет право начать?', default=False)
    is_finished = models.BooleanField('Закончил домашку?', default=False)
    is_visited = models.BooleanField('Посетил занятие?', default=False)

    def __str__(self):
        return u'{}, {}, "{}"'.format(self.student, self.module)


class ModuleLesson(models.Model):
    class Meta():
        verbose_name = 'Порядковое включение урока в модуль'
        unique_together = ('module', 'lesson')

    lesson = models.ForeignKey(Lesson)
    module = models.ForeignKey(Module)
    order = models.IntegerField()

    def __str__(self):
        return u'{} in "{}"'.format(self.lesson, self.module.title)


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

    def get_absolute_url(self):
        return "/group/%i" % self.id

    @property
    def studentgroups(self):
        studentgroups = StudentGroup.objects.filter(group=self)
        # print(sorted(studentgroups,  key=lambda m: m.average_score))
        return studentgroups

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

    @property
    def average_score(self):
        studentgrouplessons = StudentGroupLesson.objects.filter(grouplesson__group=self.group, student=self.student)
        summ = 0
        counter = 0
        for s in studentgrouplessons:
            if s.average_score:
                counter += 1
                summ += s.average_score
        if counter == 0:
            return 0
        else:
            return round(summ/counter, 1)

    @property
    def total_score(self):
        studentgrouplessons = StudentGroupLesson.objects.filter(grouplesson__group=self.group, student=self.student)
        summ = 0
        for s in studentgrouplessons:
            if s.average_score:
                summ += s.average_score
        return round(summ, 1)


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

    def __str__(self):
        return u'{}, {}, "{}"'.format(self.student, self.grouplesson.group, self.grouplesson.lesson)

    @property
    def average_score(self):
        if self.score and self.teacher_score and self.own_score:
            summ = self.score / self.max_score * 100 + self.teacher_score + self.own_score
            return round(summ/3, 1)


# ==============
# ДОМАШНИЕ ЗАДАНИЯ
# ==============
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


class LessonTask(Task):
    class Meta():
        verbose_name = 'Домашнее задание, урок'
        verbose_name_plural = 'Домашние задания, уроки'

    lesson = models.ForeignKey(Lesson)

    def __str__(self):
        return u'For {}, "{}"'.format(self.student, self.lesson)


# ==============
# БЛОКИ
# ==============
# Блоки, из которых строится занятие (контент, тест, опрос итд)
class Block(models.Model):
    def __str__(self):
        title = None

        try:
            title = self.textblock.title
        except AttributeError:
            pass

        try:
            title = self.choicequestion.question_text[:100]
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


# Включение блоков в урок
class LessonBlock(models.Model):
    class Meta():
        verbose_name = 'включение блока в урок'
        verbose_name_plural = 'включения блоков в урок'
        unique_together = ('lesson', 'block')

    lesson = models.ForeignKey(Lesson)
    block = models.ForeignKey(Block)
    order = models.IntegerField()


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

    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='choicequestions/', null=True, blank=True)

    def __str__(self):
        return self.question_text

    @property
    def rendered_question_text(self):
        return markdown.markdown(self.question_text, extensions=['markdown.extensions.extra', PyEmbedMarkdown(), 'mdx_math'])


class ChoiceQuestionOption(models.Model):
    class Meta():
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    choicequestion = models.ForeignKey(ChoiceQuestion)
    option_text = models.CharField('Вариант ответа', max_length=600, blank=True)
    option_image = models.ImageField('Картинка', upload_to='choicequestionoptions/', null=True, blank=True)
    help_text = models.CharField('Подсказка', max_length=300, blank=True)
    is_true = models.BooleanField('Правильный?')

    def __str__(self):
        return self.option_text


class FloatQuestion(Block):
    class Meta():
        verbose_name = 'задача с численным ответом'
        verbose_name_plural = 'задачи с численным ответом'

    question_text = MarkdownField('Текст вопроса')
    image = models.ImageField('Картинка', upload_to='floatquestions/', null=True, blank=True)
    answer = models.FloatField('Ответ')

    def __str__(self):
        return self.question_text

    @property
    def rendered_question_text(self):
        return markdown.markdown(self.question_text, extensions=['markdown.extensions.extra', PyEmbedMarkdown(), 'mdx_math'])


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


class FloatQuestionResult(BlockResult):
    class Meta():
        verbose_name = 'Результат ответа на задачу'
        verbose_name_plural = 'Результаты ответов на задачи'

    answer = models.FloatField('Ответ')


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