# coding=utf-8
from django.core.mail import send_mail

from quantzone import settings


def send_email(email, subject, content, plain_content=''):
    return send_mail(subject, plain_content, settings.EMAIL_HOST_USER, [email], html_message=content,
                     fail_silently=False)


def confirm_email(email, activation_key):
    current_host = settings.CURRENT_HOST
    body = u'<a title="Подтвердить" href="{}/confirm/{}" target="_blank"> Подтвердить</a>'.format(
        current_host, activation_key)
    return send_email(email, u'Подтверждение адреса электронной почты', body)


def resetpass_email(email, new_pass):
    body = u'Ваш новый пароль от аккаунта: "{}"'.format(new_pass)
    return send_email(email, u'Восстановление пароля', body)
