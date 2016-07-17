import json, urllib
from physicum import settings


class AuthError(Exception):
    def __init__(self, error, description, e=None):
        self.error = error
        self.description = description
        self.e = e
        super(AuthError, self).__init__(self.error, self.description)


class VkontakteError(AuthError):
    def __init__(self, errordict):
        self.data = errordict
        super(VkontakteError, self).__init__(errordict['error_msg'], errordict['error_code'])


def build_login_link(redirect_uri, host='', scope=''):
    raw_link = 'https://oauth.vk.com/authorize?client_id={appid}&scope={scope}&display=popup&redirect_uri={host}{redirect_uri}&response_type=code&v=5.41'
    if not host:
        host = settings.CURRENT_HOST
    if not redirect_uri.startswith('/'):
        redirect_uri = '/' + redirect_uri
    raw_link = raw_link.format(scope=scope, host=host, redirect_uri=redirect_uri, appid=settings.VKONTAKTE_APP['APPID'])
    return raw_link


def auth_code(code, redirect_uri):
    url = "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri={}{}"
    url = url.format(settings.VKONTAKTE_APP['APPID'], settings.VKONTAKTE_APP['SECRET'], code, settings.CURRENT_HOST,
                     redirect_uri)
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        raise AuthError('Auth error', 'Unathorized', e)
    response = response.read().decode()
    response = json.loads(response)
    if 'error' in response:
        raise VkontakteError(response['error'])
    return response['access_token'], response['user_id']