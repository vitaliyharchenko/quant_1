# coding=utf-8
from django import template
from utils import vkontakte
import markdown
from pyembed.markdown import PyEmbedMarkdown


register = template.Library()


# create href for vk auth
@register.simple_tag
def vk_auth_link(redirect_url):
    return vkontakte.build_login_link(redirect_url)


@register.simple_tag
def vk_profile_link(vkuserid):
    vkuserid = str(vkuserid)
    return 'http://vk.com/' + 'id' * vkuserid.isdigit() + vkuserid


@register.filter(name='markdown_rendered')
def markdown_rendered(value):
    return markdown.markdown(value, extensions=['markdown.extensions.extra', PyEmbedMarkdown(), 'mdx_math'])
