DEBUG = True
CURRENT_HOST = 'http://188.93.211.161'
ALLOWED_HOSTS = ['http://188.93.211.161']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'qdb',
        'HOST': 'localhost',
        'PASSWORD': '4203',
        'USER': 'quser',
    }
}