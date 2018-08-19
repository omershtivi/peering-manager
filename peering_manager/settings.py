# DO NOT EDIT THIS FILE!
#
# All configuration must be done in the `configuration.py` file.
# This file is part of the Peering Manager code and it will be overwritten with
# every code releases.

from __future__ import unicode_literals

import os
import socket
import random

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured


def generate_secret_key():
    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])


try:
    from peering_manager import configuration

    SECRET_KEY = getattr(configuration, 'SECRET_KEY', '')
    ALLOWED_HOSTS = getattr(configuration, 'ALLOWED_HOSTS', [])
    BASE_PATH = getattr(configuration, 'BASE_PATH', '')
    if BASE_PATH:
        BASE_PATH = BASE_PATH.strip('/') + '/'  # Enforce trailing slash only
    DEBUG = getattr(configuration, 'DEBUG', False)
    LOGIN_REQUIRED = getattr(configuration, 'LOGIN_REQUIRED', False)
    NAPALM_USERNAME = getattr(configuration, 'NAPALM_USERNAME', '')
    NAPALM_PASSWORD = getattr(configuration, 'NAPALM_PASSWORD', '')
    NAPALM_TIMEOUT = getattr(configuration, 'NAPALM_TIMEOUT', 30)
    NAPALM_ARGS = getattr(configuration, 'NAPALM_ARGS', {})
    PAGINATE_COUNT = getattr(configuration, 'PAGINATE_COUNT', 20)
    TIME_ZONE = getattr(configuration, 'TIME_ZONE', 'UTC')
    MY_ASN = getattr(configuration, 'MY_ASN', -1)
    NO_CONFIG_FILE = False

    if MY_ASN == -1:
        raise ImproperlyConfigured(
            'The MY_ASN setting must be set to a valid AS number.')

except ImportError:
    LOGIN_REQUIRED = False
    BASE_PATH = ''
    if BASE_PATH:
        BASE_PATH = BASE_PATH.strip('/') + '/'  #
    SECRET_KEY = generate_secret_key()
    ALLOWED_HOSTS = ['*']
    TIME_ZONE = 'UTC'
    NO_CONFIG_FILE = True

VERSION = '0.99-dev'


# PeeringDB URLs
PEERINGDB_API = 'https://peeringdb.com/api/'
PEERINGDB = 'https://peeringdb.com/asn/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


try:
    from peering_manager.ldap_config import *
    LDAP_CONFIGURED = True
except ImportError:
    LDAP_CONFIGURED = False

# If LDAP is configured, load the config
if LDAP_CONFIGURED:
    try:
        import ldap
        import django_auth_ldap

        # Prepend LDAPBackend to the default ModelBackend
        AUTHENTICATION_BACKENDS = [
            'django_auth_ldap.backend.LDAPBackend',
            'django.contrib.auth.backends.ModelBackend',
        ]
    except ImportError:
        raise ImproperlyConfigured(
            'LDAP authentication has been configured, but django-auth-ldap is not installed. You can remove peering_manager/ldap_config.py to disable LDAP.'
        )


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_tables2',
    'peering',
    'peeringdb',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.RequireLoginMiddleware',
]

ROOT_URLCONF = 'peering_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'peering_manager.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
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


# Django logging
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s | %(levelname)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/peering-manager.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'simple',
        },
        'peeringdb_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/peeringdb.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'simple',
        },
        'napalm_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/napalm.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'peering.manager.peering': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'peering.manager.peeringdb': {
            'handlers': ['peeringdb_file'],
            'level': 'DEBUG',
        },
        'peering.manager.napalm': {
            'handlers': ['napalm_file'],
            'level': 'DEBUG',
        },
    }
}


# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Authentication URL
LOGIN_URL = '/{}login/'.format(BASE_PATH)


# Messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR + '/static/'
STATIC_URL = '/{}static/'.format(BASE_PATH)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'project-static'),
)

# Django filters
FILTERS_NULL_CHOICE_LABEL = 'None'
FILTERS_NULL_CHOICE_VALUE = '0'

try:
    HOSTNAME = socket.gethostname()
except Exception:
    HOSTNAME = 'localhost'
