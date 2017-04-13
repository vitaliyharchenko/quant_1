from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .validators import phone_regex


# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-confirmation-mail
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

# Model, contains extra info about user.
class Profile(models.Model):

    LEARNER = 'LR'
    TEACHER = 'TH'
    PARENT = 'PR'
    PROFILE_TYPE_CHOICES = (
        (LEARNER, 'Ученик'),
        (TEACHER, 'Учитель'),
        (PARENT, 'Родитель'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(u'Дата рождения', null=True, blank=True)
    email_confirmed = models.BooleanField(u'Почта подтверждена', default=False)
    is_complete = models.BooleanField(u'Профиль активен (имеется вся информация)', default=False)
    avatar = models.ImageField(u'Аватар профиля', upload_to='avatars', null=True, blank=True)
    avatar_url = models.CharField(u'Ссылка на аватар профиля', max_length=255, null=True, blank=True)
    phone = models.CharField(u'Контактный телефон', validators=[phone_regex], blank=True, max_length=20)
    profile_type = models.CharField(u'Тип пользователя', max_length=2, choices=PROFILE_TYPE_CHOICES, default=LEARNER)

    # TODO: add city field
    # TODO: add grade field
    # TODO: add school field

    class Meta:
        verbose_name = "данные пользователя"
        verbose_name_plural = "данные пользователя"
        app_label = "users"

    def __str__(self):
        return "{}".format(self.pk)


class UserSocialAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, db_index=True)
    extra_data = models.TextField()
    is_active = models.BooleanField(u'Активна', default=True)

    class Meta:
        verbose_name = "Авторизация через соцсеть"
        verbose_name_plural = "Авторизации через соцсеть"
        app_label = "users"
        unique_together = ('provider', 'uid')

    def __str__(self):
        return str(self.user)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    confirm_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Подтверждение почтового ящика"
        verbose_name_plural = "Подтверждения почтового ящика"
        app_label = "users"

    def __str__(self):
        return str(self.email)


@receiver(pre_save, sender=User)
def unique_user_email(sender, **kwargs):
    username = kwargs['instance'].username

    if not username:
        raise ValidationError("username required")


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    # Create Profile object for every new user
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def user_profile(sender, instance, **kwargs):
    try:
        if not instance.email:
            instance.profile.email_confirmed = False
        else:
            try:
                email_confirmation = EmailConfirmation.objects.get(user=instance, email=instance.email)
                if email_confirmation.email == instance.email:
                    instance.profile.is_complete = True
                    instance.profile.email_confirmed = True
            except EmailConfirmation.DoesNotExist:
                instance.profile.is_complete = False
                instance.profile.email_confirmed = False
                instance.profile.save()

        if not instance.has_usable_password() or not instance.email or not instance.profile.email_confirmed:
            instance.profile.is_complete = False
            instance.profile.save()
        else:
            instance.profile.is_complete = True
            instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        pass
