# coding=utf-8
import random

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from utils import mailing

from utils import vkontakte
from .forms import (ChangePasswordForm, ResetPassForm, UserLoginForm,
                    UserRegistrationForm, UserUpdateForm)
from .models import User, UserActivation


@csrf_protect
def logout_view(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('index_view')
    else:
        pass


@csrf_protect
def login_view(request):
    if request.user.is_authenticated():
        return redirect('index_view')
    shortcut = lambda: render(request, 'login.html', {"form": form})
    return_path = request.META.get('HTTP_REFERER', '/')

    # regular email auth
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid:
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect(return_path)
                else:
                    messages.warning(request, "Ваш профиль не активен, проверьте почтовый ящик!")
                    return shortcut()
            else:
                messages.warning(request, "Введенные данные неверны!")
                return shortcut()
        else:
            messages.warning(request, "Введенные данные некорректны!")
            return shortcut()

    # vk return to this page with code
    elif 'code' in request.GET:
        code = request.GET['code']
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('login_view'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e))
            return redirect(return_path)
        try:
            user = User.objects.get(vkuserid=user_id)
            user.last_login = timezone.now()
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return redirect(return_path)
        except User.DoesNotExist:
            messages.warning(request, 'Такой пользователь не найден')
            return redirect(return_path)

    else:
        form = UserLoginForm(request)
        return shortcut()


def reg_view(request):
    form = UserRegistrationForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect('index_view')
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.get(email=email)

            UserActivation.objects.filter(user=user).delete()
            activation_key = signing.dumps({'email': email})
            new_activation = UserActivation(user=user, activation_key=activation_key,
                                            request_time=timezone.now())
            new_activation.save()
            mailing.confirm_email(email, activation_key)

            messages.warning(request,
                             "Пожалуйста, активируйте ваш профиль, перейдя по ссылке в письме на вашем почтовом ящике")
            # user = auth.authenticate(username=email, password=password)
            # auth.login(request, user)
            #FIXME: congrats view
            return redirect('reg_view')
        else:
            messages.warning(request, "Здесь есть неверно заполненные поля!")
            return render(request, 'reg.html', {'form': form})
    return render(request, 'reg.html', {'form': form})


def reg_confirm(request, activation_key):
    try:
        user_activation = UserActivation.objects.get(activation_key=activation_key)
    except UserActivation.DoesNotExist:
        messages.warning(request, "Неверный код активации")
        return redirect('index_view')

    user_activation.confirm_time = timezone.now()
    user_activation.save()

    user = user_activation.user
    user.is_active = True
    user.save()

    if not request.user.is_authenticated():
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        messages.success(request, "Поздравляем с успешной активацией!")
    # TODO: send thanks-message on email
    return redirect('index_view')


def user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.warning(request, "Такого пользователя нет =(")
        return redirect('index_view')
    context = {'user': user}

    if request.user.pk == user.pk:
        context['my_profile'] = True
    return render(request, 'user.html', context)


@login_required
def user_update_view(request):
    user = User.objects.get(email=request.user.email)
    form = UserUpdateForm(request.POST or None, instance=user)

    if 'code' in request.GET:
        code = request.GET['code']
        try:
            access_token, user_id = vkontakte.auth_code(code, reverse('user_update_view'))
        except vkontakte.AuthError as e:
            messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e), extra_tags='integration')
            return redirect('user_update_view')
        try:
            user = User.objects.get(vkuserid=user_id)
            messages.warning(request, 'Этот аккаунт ВКонтакте уже связан с профилем', extra_tags='integration')
            return redirect('user_update_view')
        except User.DoesNotExist:
            user = User.objects.get(email=request.user.email)
            user.vkuserid = user_id
            user.save()
            messages.success(request, "Профиль ВКонтакте прикреплен", extra_tags='integration')
            return redirect('user_update_view')

    elif request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Успешно сохранено!", extra_tags='info')
            return redirect('user_update_view')
        else:
            messages.warning(request, "Некорректные данные", extra_tags='info')
    return render(request, 'user_update.html', {'form': form, 'pass_form': ChangePasswordForm})


@login_required
def unsetvkid(request):
    user = User.objects.get(email=request.user.email)
    user.vkuserid = None
    user.save()
    messages.success(request, "Профиль ВКонтакте откреплен", extra_tags='integration')
    return redirect('user_update_view')


@login_required
def user_changepass_view(request):
    user = User.objects.get(email=request.user.email)
    pass_form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST':
        if pass_form.is_valid():
            password = pass_form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            validation = auth.authenticate(username=user.email, password=password)
            auth.login(request, validation)
            messages.success(request, "Пароль изменен", extra_tags='changepass')
        else:
            messages.warning(request, "Введенные пароли некорректны!", extra_tags='changepass')
    return redirect('user_update_view')


def resetpass_view(request):
    if request.user.is_authenticated():
        return redirect('index_view')
    form = ResetPassForm(request.POST or None)
    shortcut = lambda: render(request, 'resetpass.html', {"form": form})
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            new_pass = str(random.randint(100000, 999999))
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.warning(request, "Такого адреса нет в базе!")
                return shortcut()
            if not user.is_active:
                messages.warning(request, "Ваш аккаунт еще не активирован")
                UserActivation.objects.filter(user=user).delete()
                activation_key = signing.dumps({'email': email})
                new_activation = UserActivation(user=user, activation_key=activation_key,
                                                request_time=timezone.now())
                new_activation.save()
                mailing.confirm_email(email, activation_key)
                messages.warning(request,
                                 "Мы отправили вам новое письмо для активации")
                return shortcut()
            user.set_password(new_pass)
            user.save()
            mailing.resetpass_email(email, new_pass)
            messages.success(request, "Пароль изменен. Письмо отправлено на почту!")
    return shortcut()
