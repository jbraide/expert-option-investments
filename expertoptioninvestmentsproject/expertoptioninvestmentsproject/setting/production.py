from .base import * 

DEBUG = False
ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'expertoptioninvestments',
        'USER': 'expert',
        'PASSWORD': 'expertoptioninvestments',
        'HOST': 'localhost',
        'PORT': '',
    }
}