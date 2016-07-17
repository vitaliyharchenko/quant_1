# coding=utf-8
from django import template
from utils import vkontakte


register = template.Library()


@register.simple_tag
def vkontakte_auth_link(redirect_url):
    return vkontakte.build_login_link(redirect_url)