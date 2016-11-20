from tasks.models import Task


def logged_in_user(request):
    context = {'is_logged_in': request.user.is_authenticated()}
    if request.user.is_authenticated():
        context['current_user'] = request.user
    else:
        context['current_user'] = None
    return context


def tasks_counter(request):
    context = {}
    if request.user.is_authenticated():
        try:
            tasks = Task.objects.filter(student=request.user, is_finished=False)
            context['glob_tasks'] = tasks
        except Task.DoesNotExist:
            context['glob_tasks'] = None
    else:
        context['glob_tasks'] = None
    return context
