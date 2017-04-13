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
    list_display = ('id', 'first_name', 'last_name', 'get_birth_date', 'get_profile_type', 'get_phone', 'username',
                    'email', 'is_staff', 'get_email_confirmed', 'get_is_complete')
    list_select_related = ('profile',)

    def get_birth_date(self, instance):
        return instance.profile.birth_date
    get_birth_date.short_description = 'День рождения'

    def get_email_confirmed(self, instance):
        return instance.profile.email_confirmed
    get_email_confirmed.short_description = 'Подтверждение почты'
    get_email_confirmed.boolean = True

    def get_is_complete(self, instance):
        return instance.profile.is_complete
    get_is_complete.short_description = 'Профиль верифицирован'
    get_is_complete.boolean = True

    def get_phone(self, instance):
        return instance.profile.phone
    get_phone.short_description = 'Телефон'

    def get_profile_type(self, instance):
        return instance.profile.get_profile_type_display()
    get_profile_type.short_description = 'Тип'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(UserSocialAuth)
admin.site.register(EmailConfirmation)
