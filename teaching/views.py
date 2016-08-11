from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ChoiceQuestion, ChoiceQuestionOption, Block, BlockResult, ChoiceQuestionResult, Test, TestResult, \
    StudentStudyGroup, StudyGroup, StudyGroupLesson, Lesson


def groups_view(request):
    my_studentgroups = StudentStudyGroup.objects.filter(student=request.user)
    args = {'studentgroups': my_studentgroups}
    return render(request, 'teaching/groups.html', args)


def group_view(request, group_id):
    group = StudyGroup.objects.get(id=group_id)
    studygrouplessons = StudyGroupLesson.objects.filter(studygroup=group)
    args = {'group': group,
            'studygrouplessons': studygrouplessons}
    return render(request, 'teaching/group.html', args)


def grouplesson_view(request, group_id, lesson_id):
    group = StudyGroup.objects.get(id=group_id)
    lesson = Lesson.objects.get(id=lesson_id)
    args = {'group': group,
            'lesson': lesson}
    return render(request, 'teaching/lesson.html', args)


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


def textblock_handler(request, textblock, extra_args):
    if request.method == "POST":
        return None
    else:
        # Works if we want simple view
        args = {'textblock': textblock}
        return render(request, 'teaching/textblock.html', args)


@login_required
def block_view(request, block_id):
    try:
        block = Block.objects.get(id=block_id)
    except Block.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')

    # Works if choicequestion
    try:
        choicequestion = block.choicequestion
        return choicequestion_handler(request, choicequestion, {})
    except AttributeError:
        pass

    # Works if textblock
    try:
        textblock = block.textblock
        return textblock_handler(request, textblock, {})
    except AttributeError:
        pass

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