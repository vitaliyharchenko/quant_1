DEBUG = True
CURRENT_HOST = 'http://127.0.0.1:8000'
ALLOWED_HOSTS = ['http://127.0.0.1:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'physdb',
        'HOST': 'localhost',
        'PASSWORD': '123456',
        'USER': 'physuser',
    }
}