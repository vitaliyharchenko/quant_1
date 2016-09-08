import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
CURRENT_HOST = 'http://quant.zone'
# CURRENT_HOST = 'http://127.0.0.1:8000'
# ALLOWED_HOSTS = [
#     'http://188.93.211.161',
#     'http://127.0.0.1:8000',
#     'http://quant.zone',
#     'http://quant.zone:8000',
#     'quant.zone'
# ]
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'qdb',
        'HOST': 'localhost',
        'PASSWORD': '4203',
        'USER': 'quser',
    }
}

STATIC_URL = '/dist/'
STATIC_ROOT = os.path.join(BASE_DIR, "dist/")
