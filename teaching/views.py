from datetime import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import ChoiceQuestion, ChoiceQuestionOption, Block, BlockResult, ChoiceQuestionResult, Test, TestResult, \
    StudentGroup, Group, Lesson, GroupLesson, Task, StudentGroupLesson, GroupLessonTask, FloatQuestionResult, \
    FloatQuestion, StudentCourse, Course, StudentLesson, LessonBlock


# TODO: resolve differrent types of tasks
def tasks_view(request):
    tasks = GroupLessonTask.objects.filter(student=request.user, is_finished=False)
    args = {'tasks': tasks}
    return render(request, 'teaching/tasks.html', args)


@login_required
def courses_view(request):
    if request.user.is_staff:
        courses = Course.objects.all()
        args = {'courses': courses}
        return None
    else:
        courses = Course.objects.all()
        args = {'courses': courses}
        return render(request, 'teaching/courses.html', args)


@login_required
def course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    args = {'course': course}

    try:
        studentcourse = StudentCourse.objects.get(student=request.user, course=course)
        args['studentcourse'] = studentcourse
    except StudentCourse.DoesNotExist:
        pass

    if request.user.is_staff:
        return None
    else:
        return render(request, 'teaching/course.html', args)


@login_required
def groups_view(request):
    if request.user.is_teacher:
        groups = Group.objects.filter(teacher=request.user)
        args = {'groups': groups}
        return render(request, 'teaching/groups_teacher.html', args)
    else:
        my_studentgroups = StudentGroup.objects.filter(student=request.user)
        args = {'studentgroups': my_studentgroups}
        return render(request, 'teaching/groups.html', args)


@login_required
def group_view(request, group_id):
    group = Group.objects.get(id=group_id)
    args = {'group': group}
    if request.user == group.teacher:
        return render(request, 'teaching/group_teacher.html', args)
    else:
        return render(request, 'teaching/group.html', args)


def group_lesson_add_tasks(request, group_id, lesson_id):
    return_path = request.META.get('HTTP_REFERER', '/')

    group = Group.objects.get(id=group_id)
    lesson = Lesson.objects.get(id=lesson_id)
    grouplesson = GroupLesson.objects.get(group=group, lesson=lesson)
    studentgroups = StudentGroup.objects.filter(group=group)

    for studentgroup in studentgroups:
        try:
            studentgrouplesson = StudentGroupLesson.objects.get(grouplesson=grouplesson, student=studentgroup.student)
        except StudentGroupLesson.DoesNotExist:
            studentgrouplesson = StudentGroupLesson.objects.create(grouplesson=grouplesson,
                                                                   student=studentgroup.student)
        studentgrouplesson.has_perm = True
        studentgrouplesson.save()
        # TODO mailing student

        try:
            task = GroupLessonTask.objects.get(grouplesson=grouplesson, student=studentgroup.student)
        except Task.DoesNotExist:
            task = GroupLessonTask.objects.create(grouplesson=grouplesson, student=studentgroup.student)
        task.save()

    return redirect(return_path)


def perm_for_lesson(request, lesson):
    studentlessons = StudentLesson.objects.filter(student=request.user, lesson=lesson)
    has_perm = False
    for studentlesson in studentlessons:
        if studentlesson.has_perm == True:
            has_perm = True
    return has_perm


@login_required
def lesson_view(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if perm_for_lesson(request, lesson):
        args = {'lesson': lesson}
        return render(request, 'teaching/lesson.html', args)
    else:
        messages.warning(request, 'Нет доступа к уроку')
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)


@login_required
def lesson_final_view(request, lesson_id):
    args = {}
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        args['lesson'] = lesson

        results = []
        summ = 0
        max_summ = 0

        for lessonblock in lesson.lessonblocks:
            block_result = BlockResult.objects.filter(block=lessonblock.block, user=request.user).latest('date')
            results.append(block_result)
            summ += block_result.score
            max_summ += block_result.max_score

        args['summ'] = summ
        args['max_summ'] = max_summ

        try:
            student_lesson = StudentGroupLesson.objects.get(student=request.user, grouplesson__lesson=lesson)

            student_lesson.score = summ
            student_lesson.max_score = max_summ
            student_lesson.is_finished = True
            student_lesson.has_perm = False
            student_lesson.save()

        except StudentGroupLesson.DoesNotExist:
            pass

        try:
            tasks = GroupLessonTask.objects.filter(student=request.user, grouplesson__lesson=lesson, is_finished=False)
            for task in tasks:
                task.is_finished = True
                task.save()
        except GroupLessonTask.DoesNotExist:
            pass

        return render(request, 'teaching/lessonfinal.html', args)
    except Lesson.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')


@login_required
def lesson_block_view(request, lesson_id, block_num):
    block_num = int(block_num)
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")

    # try:
    #     block_id = lesson.blocks[block_num - 1]
    #     try:
    #         block = Block.objects.get(id=block_id)
    #     except Block.DoesNotExist:
    #         messages.warning(request, "Такого объекта нет =(")
    # except IndexError:
    #     messages.warning(request, "Такого объекта нет =(")
    # if block_num == len(lesson.blocks):
    #     extra_args = {'last_block': True}
    # else:
    #     extra_args = {'next_block_num': block_num + 1}

    try:
        lessonblock = LessonBlock.objects.get(lesson=lesson, order=block_num)
    except LessonBlock.DoesNotExist:
        messages.warning(request, "Такого объекта нет =(")

    if block_num == lesson.lessonblocks.count():
        extra_args = {'last_block': True}
    else:
        extra_args = {'next_block_num': block_num + 1}

    extra_args['lesson'] = lesson

    return block_handler(request, lessonblock.block, extra_args)


def block_handler(request, block, extra_args):
    # Works if choicequestion
    try:
        choicequestion = block.choicequestion
        return choicequestion_handler(request, choicequestion, extra_args)
    except AttributeError:
        pass

    # Works if textblock
    try:
        textblock = block.textblock
        return textblock_handler(request, textblock, extra_args)
    except AttributeError:
        pass

    # Works if floatquestion
    try:
        floatquestion = block.floatquestion
        return floatquestion_handler(request, floatquestion, extra_args)
    except AttributeError:
        pass

    return HttpResponse("Непонятный тип блока")


def choicequestion_handler(request, choicequestion, extra_args):
    if request.method == "POST":
        # Works if we catch answer
        args = extra_args
        choices = ChoiceQuestionOption.objects.filter(choicequestion=choicequestion)

        all_choices = ChoiceQuestionOption.objects.filter(choicequestion=choicequestion).values_list('id',
                                                                                                     flat=True)
        right_choices = ChoiceQuestionOption.objects.filter(choicequestion=choicequestion,
                                                            is_true=True).values_list('id', flat=True)
        our_choices = request.POST.getlist('choices')
        our_choices = list(map(int, our_choices))

        correct_choices = []
        false_not_choices = []
        false_choices = []
        correct_not_choices = []

        for choise in all_choices:
            if choise in right_choices:
                if choise in our_choices:
                    correct_choices.append(choise)
                else:
                    false_not_choices.append(choise)
            else:
                if choise in our_choices:
                    false_choices.append(choise)
                else:
                    correct_not_choices.append(choise)

        if len(false_choices) == 0 and len(false_not_choices) == 0:
            messages.success(request, 'Успешный ответ')
            args['correct_choices'] = correct_choices
        else:
            args['correct_choices'] = correct_choices
            args['false_choices'] = false_choices
            args['false_not_choices'] = false_not_choices

        if len(right_choices) == 1:
            max_score = 1
            if len(false_choices) == 0 and len(false_not_choices) == 0:
                score = 1
            else:
                score = 0
        else:
            max_score = 2
            if len(false_choices) == 0 and len(false_not_choices) == 0:
                score = 2
            elif len(false_choices) + len(false_not_choices) == 1:
                score = 1
            else:
                score = 0

        result = ChoiceQuestionResult(user=request.user, block=choicequestion, score=score, max_score=max_score,
                                      choices=our_choices)
        result.save()

        # TODO: results of test before final page
        # if extra_args['test_id'] and extra_args['last_block']:
        # test = Test.objects.get(id=extra_args['test_id'])
        #     testresult = TestResult.object.filter(user=request.user, test=test).latest(field_name='date')
        #     testresult.results.add(result)
        #     testresult.save()

        args['choicequestion'] = choicequestion
        args['choicequestionoptions'] = choices
        args['is_answered'] = True
        return render(request, 'teaching/choicequestion.html', args)
    else:
        # Works if we want simple view
        args = {'choicequestion': choicequestion,
                'choicequestionoptions': ChoiceQuestionOption.objects.filter(choicequestion=choicequestion).order_by(
                    '?')}
        return render(request, 'teaching/choicequestion.html', args)


def floatquestion_handler(request, floatquestion, extra_args):
    if request.method == "POST":
        # Works if we catch answer
        args = extra_args
        our_answer = request.POST.get('answer', '')
        our_answer = float(our_answer)
        print(our_answer)
        print(floatquestion.answer)
        max_score = 3
        if our_answer == floatquestion.answer:
            messages.success(request, 'Успешный ответ')
            score = 3
        else:
            messages.warning(request, u'Неверный ответ ({})'.format(our_answer))
            score = 0

        result = FloatQuestionResult(user=request.user, block=floatquestion, score=score, max_score=max_score,
                                     answer=our_answer)
        result.save()

        args['floatquestion'] = floatquestion
        args['is_answered'] = True
        return render(request, 'teaching/floatquestion.html', args)
    else:
        # Works if we want simple view
        args = {'floatquestion': floatquestion}
        return render(request, 'teaching/floatquestion.html', args)


def textblock_handler(request, textblock, extra_args):
    if request.method == "POST":
        result = BlockResult(user=request.user, block=textblock, score=1, max_score=1)
        result.save()

        extra_args['textblock'] = textblock
        extra_args['is_answered'] = True

        return render(request, 'teaching/textblock.html', extra_args)
    else:
        # Works if we want simple view
        extra_args['textblock'] = textblock
        return render(request, 'teaching/textblock.html', extra_args)


# пока не используется
@login_required
def block_view(request, block_id):
    try:
        block = Block.objects.get(id=block_id)
        return block_handler(request, block, {})
    except Block.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')

    return render(request, 'teaching/block.html', args)


@login_required
def test_view(request, test_id):
    args = {}
    try:
        test = Test.objects.get(id=test_id)
        args['test'] = test
        return render(request, 'teaching/test.html', args)
    except Test.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')


# Переделать так, чтобы и тест отражался через block_handler()
@login_required
def test_block_view(request, test_id, block_num):
    block_num = int(block_num)
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")

    try:
        block_id = test.blocks[block_num - 1]
    except IndexError:
        messages.warning(request, "Такого объекта нет =(")
        # TODO return 404

    try:
        block = Block.objects.get(id=block_id)
    except Block.DoesNotExist:
        messages.warning(request, "Такого объекта нет =(")

    # if block_num == 1 and request.method == "POST":
    # result = TestResult.objects.create(user=request.user, test=test)
    #     result.save()

    if block_num == len(test.blocks):
        extra_args = {
            'test_id': test_id,
            'last_block': True
        }
    else:
        extra_args = {
            'test_id': test_id,
            'next_block_num': block_num + 1
        }

    try:
        choicequestion = block.choicequestion
        return choicequestion_handler(request, choicequestion, extra_args)
    except AttributeError:
        messages.warning(request, "Это не тестовый вопрос =(")
        return redirect('index_view')


@login_required
def test_final_view(request, test_id):
    args = {}
    try:
        test = Test.objects.get(id=test_id)
        args['test'] = test
        results = []
        summ = 0
        max_summ = 0
        test_result = TestResult(user=request.user, test=test)
        test_result.save()
        for block_id in test.blocks:
            result = BlockResult.objects.filter(user=request.user, block=block_id).latest(field_name='date')
            test_result.results.add(result)
            results.append(result)
            summ += result.score
            max_summ += result.max_score
        args['results'] = results
        args['summ'] = summ
        args['max_summ'] = max_summ
        test_result.score = summ
        test_result.max_score = max_summ
        test_result.save()
        return render(request, 'teaching/testfinal.html', args)
    except Test.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')


@login_required
def test_results_view(request):
    args = {}
    results = TestResult.objects.filter(user=request.user)
    args['results'] = results
    return render(request, 'teaching/testresults.html', args)
