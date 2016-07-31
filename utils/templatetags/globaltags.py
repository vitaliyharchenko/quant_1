# coding=utf-8
from django import template
from utils import vkontakte


register = template.Library()


# create href for vk auth
@register.simple_tag
def vkontakte_auth_link(redirect_url):
    return vkontakte.build_login_link(redirect_url)


@register.simple_tag
def vkontakte_profile_link(vkuserid):
    vkuserid = str(vkuserid)
    return 'http://vk.com/' + 'id' * vkuserid.isdigit() + vkuserid