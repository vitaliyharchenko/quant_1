import ssl
import urllib
import json

from django.contrib import messages
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.conf import settings
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm, UserForm, ProfileForm
from .tokens import account_activation_token
from .models import UserSocialAuth


# Profile view with forms
@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

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
        vk_social_auth = UserSocialAuth.objects.get(user=request.user, provider='vk')
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
    user.email_user(subject, message)

    return True


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


# Success social auth point
def social_auth_complete(request, backend):
    # build link for getting access token
    url = "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri=http://{}{}"
    appid = settings.VKONTAKTE['APPID']
    secret = settings.VKONTAKTE['SECRET']
    code = request.GET['code']
    current_site = get_current_site(request)
    redirect_url = reverse('users:social_auth_complete', kwargs={'backend': backend})
    url = url.format(appid, secret, code, current_site.domain, redirect_url)

    # read response from server
    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
    except Exception as e:
        return HttpResponse(json.dumps({'error': 'Auth error, have not response', 'description': str(e)}), content_type="application/json")
    response = response.read().decode()
    response = json.loads(response)
    if 'error' in response:
        return HttpResponse(json.dumps({'error': 'Auth error, response with errors', 'description': response['error']}), content_type="application/json")

    if request.user.is_authenticated():
        # if authenticated - it is request from profile page for connect social profile
        if UserSocialAuth.objects.filter(provider=backend, uid=response['user_id']).count():
            # if this social profile is already connected - we can not connect it twice
            messages.warning(request, 'Аккаунт уже прикреплен к другому профилю.')
            return redirect('users:profile')
        else:
            # if this social profile is not connected - we can take user info from api
            api_url = "https://api.vk.com/method/users.get?fields=photo_id&access_token={}&v=5.62"
            api_url = api_url.format(response['access_token'])
            context = ssl._create_unverified_context()
            api_response = urllib.request.urlopen(api_url, context=context)
            api_response = api_response.read().decode()
            api_response = json.loads(api_response)
            # TODO: save api response

            # if this social profile is not connected - we can create this connection
            try:
                email = response['email']
            except KeyError:
                email = None

            new_social_auth = UserSocialAuth.objects.create(
                user=request.user,
                provider=backend,
                uid=response['user_id'],
                token=response['access_token'],
                email=email
            )
            new_social_auth.save()
            return redirect('users:profile')
    else:
        # if not authenticated - it is request for login
        try:
            # try to login by already existed connection
            social_auth = UserSocialAuth.objects.get(provider=backend, uid=response['user_id'])
            user = social_auth.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('users:profile')
        except UserSocialAuth.DoesNotExist:
            # if not login - try to associate by email
            try:
                email = response['email']
            except KeyError:
                email = None

            if email:
                try:
                    user = User.objects.get(email=email)
                    if user.profile.email_confirmed:
                        social_auth = UserSocialAuth.objects.create(
                            user=user,
                            provider=backend,
                            uid=response['user_id'],
                            token=response['access_token'],
                            email=email
                        )
                        social_auth.save()
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        return redirect('users:profile')
                except User.DoesNotExist:
                    pass

            # if not login and not associate to email - create profile and connection
            generic_username = backend + str(response['user_id'])
            user = User.objects.create_user(
                username=generic_username,
                email=email
            )
            user.save()

            social_auth = UserSocialAuth.objects.create(
                user=user,
                provider=backend,
                uid=response['user_id'],
                token=response['access_token'],
                email=email
            )
            social_auth.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('users:profile')
