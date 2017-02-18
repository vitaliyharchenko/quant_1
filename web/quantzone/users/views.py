from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth


# Create your views here.
@login_required
def profile_view(request):

    user = User.objects.get(id=request.user.pk)

    # Get list of existed and not existed social authorizations
    user_social_auths = list(UserSocialAuth.objects.filter(user=user).values())
    for backend in settings.SOCIAL_AUTH_BACKENDS:
        has_backend = False
        for auth in user_social_auths:
            if auth['provider'] == backend:
                has_backend = True
        if not has_backend:
            user_social_auths.append({'provider': backend, 'uid': None})

    context = {'user': user,
               'user_social_auths': user_social_auths}

    return render(request, 'users/profile.html', context)
