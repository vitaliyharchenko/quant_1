from hashlib import md5


class VKOAuth2(BaseOAuth2):
    """VKOAuth2 authentication backend"""
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'http://oauth.vk.com/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires_in', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from VK.com account"""
        fullname, first_name, last_name = self.get_user_names(
            first_name=response.get('first_name'),
            last_name=response.get('last_name')
        )
        return {'username': response.get('screen_name'),
                'email': response.get('email', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        request_data = ['first_name', 'last_name', 'screen_name', 'nickname',
                        'photo'] + self.setting('EXTRA_DATA', [])

        fields = ','.join(set(request_data))
        data = vk_api(self, 'users.get', {
            'access_token': access_token,
            'fields': fields,
        })

        if data and data.get('error'):
            error = data['error']
            msg = error.get('error_msg', 'Unknown error')
            if error.get('error_code') == 5:
                raise AuthTokenRevoked(self, msg)
            else:
                raise AuthException(self, msg)

        if data:
            data = data.get('response')[0]
            data['user_photo'] = data.get('photo')  # Backward compatibility
        return data or {}


def vk_api(backend, method, data):
    """
    Calls VK.com OpenAPI method, check:
        https://vk.com/apiclub
        http://goo.gl/yLcaa
    """
    # We need to perform server-side call if no access_token
    data['v'] = backend.setting('API_VERSION', '5.53')
    if 'access_token' not in data:
        key, secret = backend.get_key_and_secret()
        if 'api_id' not in data:
            data['api_id'] = key

        data['method'] = method
        data['format'] = 'json'
        url = 'http://api.vk.com/api.php'
        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(
            (''.join(param_list) + secret).encode('utf-8')
        ).hexdigest()
    else:
        url = 'https://api.vk.com/method/' + method

    try:
        return backend.get_json(url, params=data)
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        return None