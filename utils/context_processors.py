from users.models import User
from teaching.models import Task


def loggedin_user(request):
    context = {'is_logged_in': request.user.is_authenticated()}
    try:
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            context['current_user'] = user
        else:
            context['current_user'] = None
    except User.DoesNotExist:
        pass
    return context


def tasks_counter(request):
    context = {}
    try:
        if request.user.is_authenticated():
            user = User.objects.get(email=request.user.email)
            tasks = Task.objects.filter(student=request.user)
            context['tasks'] = tasks
        else:
            context['tasks'] = None
    except User.DoesNotExist:
        pass
    return context