from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from .forms import GroupForm, StudentGroupRelationFormSet, StudentsFormSet
from .models import Group, StudentGroupRelation


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

    # Get existing list of students
    students_data = [{'student': s.student, 'status': s.status} for s in instance.student_group_relations.order_by('status')]

    if request.method == "POST":

        group_form = GroupForm(request.POST, instance=instance)
        students_formset = StudentsFormSet(request.POST)

        if group_form.is_valid() and students_formset.is_valid():
            # Save group info
            group_form.save()
            print(students_formset.cleaned_data)

            new_students = []

            for student_form in students_formset:
                student = student_form.cleaned_data.get('student')
                status = student_form.cleaned_data.get('status')
                delete = student_form.cleaned_data.get('DELETE')

                if student and not delete:
                    new_students.append(StudentGroupRelation(group=instance, student=student, status=status))

            try:
                with transaction.atomic():
                    StudentGroupRelation.objects.filter(group=instance).delete()
                    StudentGroupRelation.objects.bulk_create(new_students)
                    print(new_students)

                    messages.success(request, 'Изменения успешно сохранены!')
            except IntegrityError:
                messages.error(request, 'Изменения не сохранены')
                return redirect('lms:group', group_id)
    else:
        group_form = GroupForm(instance=instance)
        students_formset = StudentsFormSet(initial=students_data)

    context = {
        'group': instance,
        'group_form': group_form,
        'students_formset': students_formset
    }

    return render(request, 'groups/group.html', context)
