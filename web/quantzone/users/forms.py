from random import randint

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


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

        # generate username from email
        email = obj.email
        username, _, _ = email.partition('@')

        if User.objects.filter(username=username).count():
            hash = randint(100, 999)
            username = username + str(hash)
            print(username)

        obj.username = username
        if commit:
            obj.save()
        return obj
