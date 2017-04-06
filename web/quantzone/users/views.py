import ssl
import urllib
import json
from random import randint

from django.contrib import messages
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.conf import settings
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm, UserForm, ProfileForm
from .tokens import account_activation_token
from .models import UserSocialAuth, EmailConfirmation


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

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_set_form': password_set_form,
        'vk_social_auth': vk_social_auth
    })


# Change password in Profile view
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
        appid = settings.VKONTAKTE['APPID']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        scope = 'offline,email'
        raw_link = 'https://oauth.vk.com/authorize?client_id={appid}&scope={scope}' \
                   '&display=popup&redirect_uri=http://{host}{redirect_url}&response_type=code&v=5.41'
        link = raw_link.format(scope=scope, host=current_site.domain, redirect_url=redirect_url, appid=appid)
        return redirect(link)


def get_vk_user_info(access_token):
    api_url = "https://api.vk.com/method/users.get?fields=photo_id&access_token={}&v=5.62"
    api_url = api_url.format(access_token)
    context = ssl._create_unverified_context()
    api_response = urllib.request.urlopen(api_url, context=context)
    api_response = api_response.read().decode()
    return json.loads(api_response)


def build_vk_access_link(request, backend):
    if backend == 'vk':
        url = "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://{}{}"
        appid = settings.VKONTAKTE['APPID']
        secret = settings.VKONTAKTE['SECRET']
        code = request.GET['code']
        current_site = get_current_site(request)
        redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
        url = url.format(appid, secret, code, current_site.domain, redirect_url)
        return url
    else:
        return HttpResponse(
            json.dumps({
                'error': 'Auth error, response with errors',
                'description': 'Unknown auth backend {}'.format(backend)
            }),
            content_type="application/json"
        )


# Success social auth point
def social_auth_complete(request, backend):
    # try to get access token
    try:
        context = ssl._create_unverified_context()
        url = build_vk_access_link(request, backend)
        response = urllib.request.urlopen(url, context=context)
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Auth error, have not response', 'description': str(e)}), content_type="application/json")
    response = response.read().decode()
    response = json.loads(response)

    access_token = response['access_token']
    user_social_id = response['user_id']
    try:
        email = response['email']
    except KeyError:
        email = None

    if 'error' in response:
        return HttpResponse(json.dumps({'error': 'Auth error, response with errors', 'description': response['error']}), content_type="application/json")

    # if authenticated - it is request from profile page for connect social profile
    if request.user.is_authenticated():
        # if this social profile is already connected - we can not connect it twice
        if UserSocialAuth.objects.filter(provider=backend, uid=response['user_id'], is_active=True).count():
            messages.warning(request, 'Аккаунт уже прикреплен к другому профилю.')
            return redirect('users:profile')
        # if this social profile is not connected - we can take user info from api and create connection
        else:
            api_response = get_vk_user_info(access_token)

            new_social_auth = UserSocialAuth.objects.create(
                user=request.user,
                provider=backend,
                uid=user_social_id,
                token=access_token,
                email=email,
                extra_data=api_response
            )
            new_social_auth.save()
            return redirect('users:profile')
    # if not authenticated - it is request for login
    else:
        # try to login by already existed connection
        try:
            social_auth = UserSocialAuth.objects.get(provider=backend, uid=response['user_id'])

            # renew extra data
            api_response = get_vk_user_info(response['access_token'])
            social_auth.extra_data = api_response
            social_auth.is_active = True
            social_auth.save()

            user = social_auth.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('users:profile')
        # if not login - try to associate by email
        except UserSocialAuth.DoesNotExist:
            if email:
                try:
                    user = User.objects.get(email=email)
                    if user.profile.email_confirmed:
                        api_response = get_vk_user_info(response['access_token'])
                        new_social_auth = UserSocialAuth.objects.create(
                            user=user,
                            provider=backend,
                            uid=response['user_id'],
                            token=response['access_token'],
                            email=email,
                            extra_data=api_response
                        )
                        new_social_auth.save()
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        return redirect('users:profile')
                except User.DoesNotExist:
                    pass

            # if not associate to email - create profile and connection
            generic_username = backend + str(user_social_id)

            # if username conflict - add random string
            if User.objects.filter(username=generic_username).count():
                rand_hash = randint(100, 999)
                generic_username += str(rand_hash)

            user = User.objects.create_user(
                username=generic_username,
                email=email
            )
            user.save()

            api_response = get_vk_user_info(response['access_token'])
            new_social_auth = UserSocialAuth.objects.create(
                user=user,
                provider=backend,
                uid=user_social_id,
                token=access_token,
                email=email,
                extra_data=api_response
            )
            new_social_auth.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('users:profile')


# Deassociate user email
@login_required
def social_auth_delete(request, backend):
    # TODO: deactivate social auth, but still have in DB
    user = User.objects.get(pk=request.user.pk)
    if not user.has_usable_password() or not user.email or not user.profile.email_confirmed:
        messages.success(request, 'Невозможно отвязать социальный профиль, у вас не остается возможностей для входа!')
        return redirect('users:profile')
    social_auth = UserSocialAuth.objects.get(provider=backend, user=request.user)
    social_auth.is_active = False
    social_auth.save()
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
