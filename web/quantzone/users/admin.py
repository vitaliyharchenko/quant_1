from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import EmailConfirmation, Profile, UserSocialAuth


# Adding Profile inline to default Django Admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(UserSocialAuth)
admin.site.register(EmailConfirmation)
