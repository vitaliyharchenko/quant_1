def logged_in_user(request):
    context = {'is_logged_in': request.user.is_authenticated()}
    if request.user.is_authenticated():
        context['current_user'] = request.user
    else:
        context['current_user'] = None
    return context
