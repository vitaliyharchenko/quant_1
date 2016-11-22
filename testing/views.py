from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from testing.models import Test, TestBlockRelation
from blocks.views import block_handler
from results.models import TestResult, BlockResult


# Create your views here.
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
        test_block_relation = TestBlockRelation.objects.get(test=test, order=block_num)
    except TestBlockRelation.DoesNotExist:
        messages.warning(request, "Такого объекта нет =(")

    blocks_count = test.test_block_relations().count()

    extra_args = {}

    if block_num == blocks_count:
        extra_args['last_block'] = True
    else:
        extra_args['next_block_num'] = block_num + 1

    extra_args['test'] = test
    extra_args['block_num'] = block_num
    extra_args['blocks_count'] = blocks_count

    return block_handler(request, test_block_relation.block, extra_args)


@login_required
def test_final_view(request, test_id):
    #TODO: save results
    args = {}
    try:
        test = Test.objects.get(id=test_id)
        args['test'] = test
        results = []
        summ = 0
        max_summ = 0
        relations = test.test_block_relations
        for test_block_relation in relations:
            block_result = BlockResult.objects.filter(block=test_block_relation.block, student=request.user).latest(
                'date')
            results.append(block_result)
            summ += block_result.score
            max_summ += block_result.max_score
        args['results'] = results
        args['summ'] = summ
        args['max_summ'] = max_summ

        test_result = TestResult.objects.create(student=request.user, test=test, score=summ, max_score=max_summ)
        test_result.save()
        return render(request, 'teaching/test_final.html', args)
    except Test.DoesNotExist:
        # TODO: add 404 page
        messages.warning(request, "Такого объекта нет =(")
        return redirect('index_view')
