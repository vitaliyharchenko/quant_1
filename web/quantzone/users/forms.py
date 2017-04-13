from random import randint

import phonenumbers
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from .models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            print(self.request)
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите существующий почтовый адрес.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).count():
            raise ValidationError("Почтовый адрес уже занят")
        return email

    def save(self, commit=True):
        obj = super(SignUpForm, self).save(commit=False)

        # generate username from email (all before @)
        email = obj.email
        username, _, _ = email.partition('@')

        # if username conflict - add random string
        if User.objects.filter(username=username).count():
            rand_hash = randint(100, 999)
            username += str(rand_hash)

        obj.username = username

        if commit:
            obj.save()

        return obj


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        # Check if that email is in use already
        if email and User.objects.filter(email=email).exclude(username=username).count():
            self.add_error('email', u"Почтовый адрес уже занят")

        # Check if that email is empty
        if not email:
            self.add_error('email', u"Почтовый адрес не может быть пустым")

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'email_confirmed', 'avatar', 'phone')

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            parsed_phone = phonenumbers.parse(phone, "RU")
            phone_formated = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            phone_is_valid = phonenumbers.is_valid_number(parsed_phone)
            if phone_is_valid:
                return phone_formated
            else:
                raise ValidationError("Укажите корректный номер")
        else:
            return None
