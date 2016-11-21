from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StudentTeacherRelation


# Create your views here.
@login_required
def cabinet_view(request):
    if request.user.is_teacher:
        student_teachers = StudentTeacherRelation.objects.filter(teacher=request.user)
        args = {'student_teachers': student_teachers}
        return render(request, 'teaching/cabinet.html', args)
    else:
        messages.warning(request, 'Войдите как учитель')
        return redirect('index_view')
