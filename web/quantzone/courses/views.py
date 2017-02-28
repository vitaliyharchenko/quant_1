from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Course, StudentCourseRelation


@login_required
def courses_view(request):
    courses = Course.objects.all()
    args = {'courses': courses}
    return render(request, 'teaching/courses.html', args)


@login_required
def course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    args = {'course': course}

    try:
        student_course = StudentCourseRelation.objects.get(student=request.user, course=course)
        args['student_course'] = student_course
    except StudentCourseRelation.DoesNotExist:
        pass

    return render(request, 'teaching/course.html', args)
