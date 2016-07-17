from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from utils import vkontakte
from .models import User


# Create your views here.
def index_view(request):
    shortcut = lambda: render(request, 'index.html')
    return shortcut()


def logout_view(request):
    auth.logout(request)
    return redirect('index_view')


def login_view(request):
    if 'code' in request.GET:
        code = request.GET['code']
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('login_view'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e))
            return render(request, 'index.html')
        try:
            user = User.objects.get(vkuserid=user_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return render(request, 'index.html')
        except User.DoesNotExist:
            messages.warning(request, 'Такой пользователь не найден')
            return render(request, 'index.html')