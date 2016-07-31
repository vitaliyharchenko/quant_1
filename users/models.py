# coding=utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            bdate=extra_fields.pop("bdate", False)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)

    vkuserid = models.IntegerField(unique=True, null=True, blank=True)

    bdate = models.DateField()
    first_name = models.CharField(u'Имя', max_length=120)
    last_name = models.CharField(u'Фамилия', max_length=120)
    sex = models.CharField(max_length=1, choices=(('m', 'мужской'), ('f', 'женский')), verbose_name='Пол')

    is_active = models.BooleanField(u'Активный', default=True)
    is_staff = models.BooleanField(u'Доступ к админке', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'bdate', 'sex']
    REGISTRATION_FIELDS = ['email'] + ['first_name', 'last_name', 'bdate', 'sex']
    UPDATE_FIELDS = REQUIRED_FIELDS

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_absolute_url(self):
        return "/users/%i" % self.id

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    def __str__(self):
        return u'{} {} ({})'.format(self.first_name, self.last_name, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class UserActivation(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=100, blank=True)
    request_time = models.DateTimeField(default=timezone.now)
    confirm_time = models.DateTimeField('Дата активации', blank=True, null=True)

    def __str__(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = u'Активации'