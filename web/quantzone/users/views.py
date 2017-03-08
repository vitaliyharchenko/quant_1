from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm
from .tokens import account_activation_token


# Create your views here.
@login_required
def profile(request):

    user = User.objects.get(id=request.user.pk)

    # Get list of existed and not existed social authorizations
    # user_social_auths = list(UserSocialAuth.objects.filter(user=user).values())
    # for backend in settings.SOCIAL_AUTH_BACKENDS:
    #     has_backend = False
    #     for auth in user_social_auths:
    #         if auth['provider'] == backend:
    #             has_backend = True
    #     if not has_backend:
    #         user_social_auths.append({'provider': backend, 'uid': None})

    context = {'user': user}

    return render(request, 'users/profile.html', context)


# Registration starting point
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('users:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


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
        login(request, user)
        return redirect('users:profile')
    else:
        return render(request, 'users/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'users/account_activation_send.html')
