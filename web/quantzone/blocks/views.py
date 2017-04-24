from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Block


# Block view for testing
@login_required()
def block(request, block_id):
    context = {
        'instance': Block.objects.get(pk=block_id)
    }
    return render(request, 'blocks/block.html', context)