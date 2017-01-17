import json
import ssl
import urllib

from quantzone import settings


# error in connection with vk server
class AuthError(Exception):
    def __init__(self, error, description, e=None):
        self.error = error
        self.description = description
        self.e = e
        super(AuthError, self).__init__(self.error, self.description, self.e)


# create login vk link
def build_login_link(redirect_uri, scope=''):
    raw_link = "https://oauth.vk.com/authorize?client_id={appid}&scope={scope}&display=popup&redirect_uri={host}{redirect_uri}&response_type=code&v=5.41"
    if not redirect_uri.startswith('/'):
        redirect_uri = '/' + redirect_uri
    raw_link = raw_link.format(scope=scope, host=settings.CURRENT_HOST, redirect_uri=redirect_uri, appid=settings.VKONTAKTE_APP['APPID'])
    return raw_link


# auth by code, return user vkid
def auth_code(code, redirect_uri):
    url = "https://oauth.vk.com/access_token?client_id={}&client_secret={}&code={}&redirect_uri={}{}"
    url = url.format(settings.VKONTAKTE_APP['APPID'], settings.VKONTAKTE_APP['SECRET'], code, settings.CURRENT_HOST,
                     redirect_uri)
    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
    except Exception as e:
        raise AuthError('Auth error', 'Unauthorized', e)
    response = response.read().decode()
    response = json.loads(response)
    if 'error' in response:
        raise AuthError('VK error', response['error']['error_msg'], response['error']['error_code'])
    return response['access_token'], response['user_id']
