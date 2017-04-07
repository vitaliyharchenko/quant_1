import phonenumbers
from random import randint

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from .models import Profile


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
        phone_number = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
        return phone_number
