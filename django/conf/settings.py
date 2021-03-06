"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from .get_secret import get_secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret(os.getenv('DJANGO_SK_FILE'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOST_NAME = os.getenv('HOST_NAME')
HOST_IP = os.getenv('HOST_IP')
ALLOWED_HOSTS = ['apache', HOST_NAME, HOST_IP]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret(os.getenv('POSTGRES_DB_FILE')),
        'USER': get_secret(os.getenv('POSTGRES_USER_FILE')),
        'PASSWORD': get_secret(os.getenv('POSTGRES_PASSWORD_FILE')),
        'HOST': 'postgres',
        'PORT': '5432',
        'ATOMIC_REQUEST': True,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_L10N = False # disable datetime and numeric internationalization

USE_TZ = True

# Параметры ввода и вывода дат: задано вручную (при отключении USE_L10N)
DATE_FORMAT = "d.m.Y"
DATE_INPUT_FORMATS = ['%d.%m.%Y']
SHORT_DATE_FORMAT = "d.m.Y"

DATETIME_FORMAT = "d.m.Y H:i:s"
DATETIME_INPUT_FORMATS = ["%d.%m.%Y %H:%M:%S"]
SHORT_DATETIME_FORMAT = "d.m.Y H:M:s"

TIME_FORMAT = "H:M"
TIME_INPUT_FORMATS = ["%H:%M"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'

# crispy_forms settings:
INSTALLED_APPS += ['crispy_forms',]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# user settings
INSTALLED_APPS = ['user.apps.UserConfig',] + INSTALLED_APPS
AUTH_USER_MODEL = 'user.AdvUser'
LOGIN_URL = '/accounts/login/' # адрес, ведущий на страницу входа
LOGIN_REDIRECT_URL = '/accounts/profile/' # адрес, на который произойдет перенаправление после входа
LOGOUT_REDIRECT_URL = '/' # адрес, на который произойдет перенаправление после выхода

# core settings
INSTALLED_APPS += ['core.apps.CoreConfig',]

# Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
MAILING_LIST_FROM_EMAIL = 'noreply@mailer.com'
MAILING_LIST_LINK_DOMAIN = HOST_NAME

# selery settings
INSTALLED_APPS += ['django_celery_results',]
CELERY_BROKER_URL = 'redis://redis'
CELERY_RESULT_BACKEND = 'django-db'

# API settings
# django_rest_framework settings
INSTALLED_APPS += ['rest_framework',]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '60/minute',
        'anon': '30/minute',
    }
}
