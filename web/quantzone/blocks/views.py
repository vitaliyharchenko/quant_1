from blocks.models import Block, ChoiceBlock, FloatBlock, TextBlock
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from results.models import BlockResult, ChoiceBlockResult, FloatBlockResult

from nodes.models import Lesson
from .models import ChoiceBlockOption, LessonBlockRelation


@login_required
def lesson_block_view(request, lesson_id, block_num):
    block_num = int(block_num)
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")

    try:
        lesson_block_relation = LessonBlockRelation.objects.get(lesson=lesson, order=block_num)
    except LessonBlockRelation.DoesNotExist:
        messages.warning(request, "Такого объекта нет =(")

    blocks_count = lesson.lesson_block_relations.count()

    extra_args = {}

    if block_num == blocks_count:
        extra_args['last_block'] = True
    else:
        extra_args['next_block_num'] = block_num + 1

    extra_args['lesson'] = lesson
    extra_args['block_num'] = block_num
    extra_args['blocks_count'] = blocks_count

    return block_handler(request, lesson_block_relation.block, extra_args)


# ==============
# Block handlers
# ==============
def block_handler(request, block, extra_args):
    try:
        choice_block = ChoiceBlock.objects.get(pk=block.pk)
        return choice_block_handler(request, choice_block, extra_args)
    except ChoiceBlock.DoesNotExist:
        pass

    try:
        text_block = TextBlock.objects.get(pk=block.pk)
        return text_block_handler(request, text_block, extra_args)
    except TextBlock.DoesNotExist:
        pass

    try:
        float_block = FloatBlock.objects.get(pk=block.pk)
        return float_block_handler(request, float_block, extra_args)
    except FloatBlock.DoesNotExist:
        pass

    return HttpResponse("Непонятный тип блока")


def choice_block_handler(request, choice_block, extra_args):
    if request.method == "POST":
        # Works if we catch answer
        args = extra_args
        choices = ChoiceBlockOption.objects.filter(choice_block=choice_block)

        all_choices = choices.values_list('id', flat=True)
        right_choices = choices.filter(is_true=True).values_list('id', flat=True)
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
            # messages.success(request, 'Успешный ответ')
            args['correct_choices'] = correct_choices
        else:
            args['correct_choices'] = correct_choices
            args['false_choices'] = false_choices
            args['false_not_choices'] = false_not_choices

        if len(right_choices) == 1:
            # FIXME: define max score in block model
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

        result = ChoiceBlockResult(student=request.user, block=choice_block, score=score, max_score=max_score,
                                   choices=our_choices)
        result.save()

        args['choice_block'] = choice_block
        args['choice_block_options'] = choices
        args['is_answered'] = True
        return render(request, 'teaching/choice_block.html', args)
    else:
        args = extra_args
        args['choice_block'] = choice_block
        args['choice_block_options'] = ChoiceBlockOption.objects.filter(choice_block=choice_block)
        return render(request, 'teaching/choice_block.html', args)


def float_block_handler(request, float_block, extra_args):
    if request.method == "POST":
        # Works if we catch answer
        our_answer = request.POST.get('answer', '')
        our_answer = float(our_answer)
        max_score = 3
        if our_answer == float_block.answer:
            message = u'Правильный ответ'
            score = 3
        else:
            message = u'Неверный ответ, должно было получиться {}'.format(float_block.answer)
            score = 0

        result = FloatBlockResult(student=request.user, block=float_block, score=score, max_score=max_score,
                                  answer=our_answer)
        result.save()

        return HttpResponse(message)
    else:
        # Works if we want simple view
        args = extra_args
        args['float_block'] = float_block
        return render(request, 'teaching/float_block.html', args)


def text_block_handler(request, text_block, extra_args):
    if request.method == "POST":
        result = BlockResult(student=request.user, block=text_block, score=1, max_score=1)
        result.save()
        return HttpResponse('OK')
    else:
        # Works if we want simple view
        extra_args['text_block'] = text_block
        return render(request, 'teaching/text_block.html', extra_args)


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
