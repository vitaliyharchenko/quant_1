from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "данные пользователя"

    def __str__(self):
        return "{}".format(self.pk)


@receiver(pre_save, sender=User)
def unique_user_email(sender, **kwargs):
    email = kwargs['instance'].email
    username = kwargs['instance'].username

    if not username:
        raise ValidationError("username required")

    if not email:
        raise ValidationError("email required")

    # TODO: must be in tests
    # if sender.objects.filter(email=email).exclude(username=username).count():
    #     raise ValidationError("email needs to be unique")


# Create Profile object for every new user
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
