from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "данные пользователя"

    def __str__(self):
        return "{}".format(self.pk)


@receiver(pre_save, sender=User)
def unique_user_email(sender, **kwargs):
    email = kwargs['instance'].email
    username = kwargs['instance'].username

    if not email:
        raise ValidationError("email required")

    if sender.objects.filter(email=email).exclude(username=username).count():
        raise ValidationError("email needs to be unique")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
