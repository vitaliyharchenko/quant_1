from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import GroupCreationForm
from .models import Group


# Create your views here.
def groups(request):
    groups = Group.objects.filter(owner=request.user)

    if request.method == "POST":
        form = GroupCreationForm(request.POST)
        if form.is_valid:
            form.save()
            form = GroupCreationForm()
        else:
            messages.warning(request, "Введенные данные некорректны!")
    else:
        form = GroupCreationForm(instance=Group(owner=request.user))

    return render(request, 'groups/groups.html', {'form': form,
                                                  'groups': groups})
