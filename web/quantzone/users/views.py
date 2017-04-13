import json
import ssl
import urllib
from random import randint

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import HttpResponse, redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import ProfileForm, SignUpForm, UserForm
from .models import EmailConfirmation, UserSocialAuth
from .tokens import account_activation_token


# Login view
def login(request):
    # ready for login from any page on site
    return_path = request.META.get('HTTP_REFERER', '/')
    login_path = 'http://{}{}'.format(get_current_site(request), reverse('users:login'))
    if return_path == login_path:
        return_path = reverse('users:profile')

    if request.user.is_authenticated():
        return redirect(return_path)

    if request.method == "POST":
        form = AuthenticationForm(request.POST or None)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(return_path)
            else:
                messages.warning(request, "Введенные данные неверны!")
        else:
            messages.warning(request, "Введенные данные некорректны!")
    else:
        form = AuthenticationForm(request)

    return render(request, 'users/login.html', {"form": form})


# Profile view with forms
@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        password_set_form = SetPasswordForm(request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Изменения успешно сохранены!')
            return redirect('users:profile')
        else:
            messages.warning(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_set_form = SetPasswordForm(request.user)

    try:
        vk_social_auth = UserSocialAuth.objects.get(user=request.user, provider='vk', is_active=True)
    except UserSocialAuth.DoesNotExist:
        vk_social_auth = None

    try:
        fb_social_auth = UserSocialAuth.objects.get(user=request.user, provider='fb', is_active=True)
    except UserSocialAuth.DoesNotExist:
        fb_social_auth = None

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_set_form': password_set_form,
        'vk_social_auth': vk_social_auth,
        'fb_social_auth': fb_social_auth
    })


# Change password in Profile view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('users:profile')
        else:
            messages.warning(request, 'Пожалуйста, исправьте ошибки.')
    return redirect('users:profile')


# Registration starting point
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send email
            send_activation_email(request, user)

            return redirect('users:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# Method, that send activation email to user
def send_activation_email(request, user):
    current_site = get_current_site(request)
    subject = 'Активируйте ваш аккаунт'
    message = render_to_string('email/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message,
                     fail_silently=True)


# Success signup page
def account_activation_sent(request):
    return render(request, 'users/account_activation_send.html')


# Send activation for existing user
def send_activation(request):
    send_activation_email(request, request.user)
    return redirect('users:account_activation_sent')


# Activate user
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        try:
            email_confirmation = EmailConfirmation.objects.get(user=user)
            confirmed_email = email_confirmation.email
            if confirmed_email != user.email:
                email_confirmation.email = user.email
                email_confirmation.save()
        except EmailConfirmation.DoesNotExist:
            email_confirmation = EmailConfirmation.objects.create(
                user=user,
                email=user.email
            )
            email_confirmation.save()

        user.is_active = True
        user.profile.email_confirmed = True
        user.save()

        if not request.user.is_authenticated():
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        return redirect('users:account_activation_success')
    else:
        return render(request, 'users/account_activation_invalid.html')


# Success email activation point
def account_activation_success(request):
    return render(request, 'users/account_activation_success.html')


# ===========
# SOCIAL AUTH
# ===========

# Social auth starting point
def social_auth(request, backend):
    if backend == 'vk':
        app_id = settings.VKONTAKTE['APP_ID']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        scope = 'offline,email'
        raw_link = 'https://oauth.vk.com/authorize?client_id={app_id}&scope={scope}' \
                   '&display=popup&redirect_uri=http://{host}{redirect_url}&response_type=code&v=5.41'
        link = raw_link.format(scope=scope, host=current_site.domain, redirect_url=redirect_url, app_id=app_id)
        return redirect(link)
    elif backend == 'fb':
        app_id = settings.FACEBOOK['APP_ID']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        scope = 'email'
        raw_link = "https://www.facebook.com/v2.8/dialog/oauth?client_id={app_id}&scope={scope}&" \
                   "redirect_uri=http://{host}{redirect_url}&response_type=code"
        link = raw_link.format(scope=scope, host=current_site.domain, redirect_url=redirect_url, app_id=app_id)
        return redirect(link)


def get_social_user_info(access_token, backend):
    if backend == 'vk':
        api_url = "https://api.vk.com/method/users.get?fields={}&access_token={}&v=5.62"
        # https://vk.com/dev/objects/user
        fields = "about,activities,bdate,city,connections,contacts,country,education,first_name,followers_count," \
                 "has_photo,interests,last_name,occupation,personal,photo_id,photo_max_orig,quotes,schools,sex," \
                 "universities"
        api_url = api_url.format(fields, access_token)
        context = ssl._create_unverified_context()
        api_response = urllib.request.urlopen(api_url, context=context)
        api_response = api_response.read().decode()
        json_response = json.loads(api_response)
        response = json_response['response'][0]
        return response['id'], response
    elif backend == 'fb':
        api_url = "https://graph.facebook.com/me?fields={}&access_token={}&debug=all"
        # https://vk.com/dev/objects/user
        fields = "id,email,first_name,gender,last_name,link,locale,name,timezone,updated_time,verified," \
                 "picture.type(large)"
        api_url = api_url.format(fields, access_token)
        context = ssl._create_unverified_context()
        api_response = urllib.request.urlopen(api_url, context=context)
        api_response = api_response.read().decode()
        json_response = json.loads(api_response)
        response = json_response
        return response['id'], response


def build_social_access_link(request, backend):
    if backend == 'vk':
        url = "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://{}{}"
        app_id = settings.VKONTAKTE['APP_ID']
        secret = settings.VKONTAKTE['SECRET']
        code = request.GET['code']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        url = url.format(app_id, secret, code, current_site.domain, redirect_url)
        return url
    elif backend == 'fb':
        url = "https://graph.facebook.com/v2.8/oauth/access_token?client_id={}&client_secret={}" \
              "&code={}&redirect_uri=http://{}{}"
        app_id = settings.FACEBOOK['APP_ID']
        secret = settings.FACEBOOK['SECRET']
        code = request.GET['code']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        url = url.format(app_id, secret, code, current_site.domain, redirect_url)
        return url
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Auth error, response with errors',
                'description': 'Unknown auth backend {}'.format(backend)
            }),
            content_type="application/json"
        )


# Method for getting avatar_url and set to profile
def update_avatar_info(extra_data, user):
    if not user.profile.avatar_url:
        if extra_data.__class__.__name__ != 'dict':
            dict_data = eval(extra_data)
        else:
            dict_data = extra_data

        try:
            avatar_url = dict_data['photo_max_orig']
        except KeyError:
            try:
                avatar_url = dict_data['picture']['data']['url']
            except KeyError:
                avatar_url = None
        user.profile.avatar_url = avatar_url
        user.profile.save()


# Success social auth point
def social_auth_complete(request, backend):
    # try to get access token
    try:
        context = ssl._create_unverified_context()
        url = build_social_access_link(request, backend)
        response = urllib.request.urlopen(url, context=context)
        response = response.read().decode()
        response = json.loads(response)

        if 'error' in response:
            return HttpResponse(
                json.dumps({'error': 'Auth error, response with errors', 'description': response['error']}),
                content_type="application/json")

        access_token = response['access_token']
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Auth error, have not response', 'description': str(e)}), content_type="application/json")

    # try to get user_id and extra data
    social_user_id, extra_data = get_social_user_info(access_token, backend)

    # try to det user email
    try:
        if backend == 'vk':
            email = response['email']
        elif backend == 'fb':
            email = extra_data['email']
    except KeyError:
        email = None

    if 'error' in response:
        return HttpResponse(json.dumps({'error': 'Auth error, response with errors', 'description': response['error']}), content_type="application/json")

    # if authenticated - it is request from profile page for connect social profile
    if request.user.is_authenticated():
        # if this social profile is already connected - we can not connect it twice
        try:
            existing_social_auth = UserSocialAuth.objects.get(provider=backend, uid=social_user_id)
            if request.user != existing_social_auth.user:
                messages.warning(request, 'Аккаунт уже прикреплен к другому профилю.')
                return redirect('users:profile')
            else:
                existing_social_auth.extra_data = extra_data
                existing_social_auth.is_active = True
                existing_social_auth.save()

                update_avatar_info(extra_data, request.user)

                messages.success(request, 'Аккаунт успешно прикреплен.')
                return redirect('users:profile')
        except UserSocialAuth.DoesNotExist:
            new_social_auth = UserSocialAuth.objects.create(
                user=request.user,
                provider=backend,
                uid=social_user_id,
                token=access_token,
                email=email,
                extra_data=str(extra_data)
            )
            new_social_auth.save()

            update_avatar_info(extra_data, request.user)

            messages.success(request, 'Аккаунт успешно прикреплен.')
            return redirect('users:profile')
    # if not authenticated - it is request for login
    else:
        # try to login by already existed connection
        try:
            social_auth = UserSocialAuth.objects.get(provider=backend, uid=social_user_id)

            # renew extra data
            social_auth.extra_data = extra_data
            social_auth.is_active = True
            social_auth.save()

            user = social_auth.user

            update_avatar_info(extra_data, user)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return redirect('users:profile')
        # if not login - try to associate by email
        except UserSocialAuth.DoesNotExist:
            if email:
                try:
                    user = User.objects.get(email=email)
                    if user.profile.email_confirmed:
                        new_social_auth = UserSocialAuth.objects.create(
                            user=user,
                            provider=backend,
                            uid=social_user_id,
                            token=access_token,
                            email=email,
                            extra_data=str(extra_data)
                        )
                        new_social_auth.save()
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)

                        messages.success(request,
                                         'Ваш социальный аккаунт привязан на основании сответствия почтового адреса')
                        return redirect('users:profile')
                except User.DoesNotExist:
                    pass

            # if not associate to email - create profile and connection
            generic_username = backend + str(social_user_id)

            # if username conflict - add random string
            if User.objects.filter(username=generic_username).count():
                rand_hash = randint(100, 999)
                generic_username += str(rand_hash)

            user = User.objects.create_user(
                username=generic_username,
                email=email
            )
            user.save()

            update_avatar_info(extra_data, user)

            new_social_auth = UserSocialAuth.objects.create(
                user=user,
                provider=backend,
                uid=social_user_id,
                token=access_token,
                email=email,
                extra_data=str(extra_data)
            )
            new_social_auth.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)

            messages.success(request, 'Ваш аккаунт создан на основании данных соцсети.')
            return redirect('users:profile')


# Deassociate user email
@login_required
def social_auth_deassociate(request, backend):
    user = User.objects.get(pk=request.user.pk)
    if not user.has_usable_password() or not user.email or not user.profile.email_confirmed:
        messages.warning(request, 'Невозможно отвязать социальный профиль, у вас не остается возможностей для входа!')
        return redirect('users:profile')
    social_auth = UserSocialAuth.objects.get(provider=backend, user=request.user)
    social_auth.is_active = False
    social_auth.save()

    # if disconnect - delete avatar
    if backend == 'vk':
        try:
            extra_data = social_auth.extra_data
            dict_data = eval(extra_data)
            avatar_url = dict_data['photo_max_orig']
        except KeyError:
            avatar_url = None
    elif backend == 'fb':
        try:
            extra_data = social_auth.extra_data
            dict_data = eval(extra_data)
            avatar_url = dict_data['picture']['data']['url']
        except KeyError:
            avatar_url = None
    if user.profile.avatar_url == avatar_url:
        user.profile.avatar_url = None
        user.profile.save()

    return redirect('users:profile')


# Reset password starting point
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.warning(request, 'Такого почтового ящика нет в базе.')
                return render(request, 'users/password_reset.html', {'form': form})

            current_site = get_current_site(request)
            subject = 'Сброс пароля'
            message = render_to_string('email/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=message,
                      fail_silently=True)
            return redirect('users:password_reset_done')
        else:
            messages.warning(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})


# Success start reset password
def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')


# Link in reset password email
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('users:password_reset_complete')
            else:
                messages.warning(request, 'Исправьте ошибки')
        else:
            form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.warning(request, 'Что-то пошло не так')
        return render(request, 'users/password_reset_incomplete.html')


# Success finish reset password
def password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')
