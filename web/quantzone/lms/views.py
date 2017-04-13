from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import GroupForm
from .models import Group


# All teacher groups
def groups(request):
    all_groups = Group.objects.filter(owner=request.user)

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid:
            form.save()
            form = GroupForm()
        else:
            messages.warning(request, "Введенные данные некорректны!")
    else:
        form = GroupForm(instance=Group(owner=request.user))

    return render(request, 'groups/groups.html', {'form': form,
                                                  'groups': all_groups})


def group(request, group_id):
    instance = Group.objects.get(pk=group_id)

    if request.method == "POST":
        form = GroupForm(request.POST or None, instance=instance)
        if form.is_valid:
            form.save()
        else:
            messages.warning(request, "Введенные данные некорректны!")
    else:
        form = GroupForm(instance=instance)

    return render(request, 'groups/group.html', {'group': instance, 'form': form})
