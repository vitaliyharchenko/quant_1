from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Block


# Block view for testing
@login_required()
def block(request, block_id):
    instance = Block.objects.get_subclass(pk=block_id)
    if instance.class_name() == 'TextBlock':
        context = {
            'instance': instance
        }
        return render(request, 'blocks/text_block.html', context)
    elif instance.class_name() == 'ChoiceBlock':
        context = {
            'instance': instance
        }
        return render(request, 'blocks/choice_block.html', context)
    else:
        return
