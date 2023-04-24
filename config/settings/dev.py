"""dev.py
settings for dev environments

WARNING: This settings must not be used in production
to use this settings: set your the environment variable ENV=dev
"""
from config.settings.base import *
from django.core.exceptions import *
import environ
import os

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    '008c-41-184-7-73.eu.ngrok.io'
]

# DEV APPS
# NOT ALL LIBRARIES
# HERE MIGHT MAKE IT TO
# STAGING OR PRODUCTION
DEV_APPS = [
    'knox',
    'rest_framework_simplejwt',
    'drf_standardized_errors'
]
INSTALLED_APPS.extend(DEV_APPS)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, '.env-dev')
env.read_env(env_file)


def getvar(name: str):
    '''tries to get the environmental vairable using\
         env or getenv.

        env is bound to this settings while getenv is global.
        getenv gets global, dynamic or user specific environmental\
            variables.
    '''
    # first try getting the variable using env
    # if failed, then use getenv
    try:
        var = env(name)
    except ImproperlyConfigured:
        var = getenv(name)
    return var


SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getvar('DB_NAME'),
        'USER': getvar('DB_USER'),
        'PASSWORD': getvar('DB_PASSWORD'),
        'HOST': getvar('DB_HOST'),
        'PORT': getvar('DB_PORT')
    }
}

CORS_ORIGIN_ALLOW_ALL = True

OAUTH2_PROVIDER = {
    # parses OAuth2 data from application/json requests
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
         #'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
         'services.authiam.backends.OAuth2ClientCredentialAuthentication',
    ),

    # exception handler
    #'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler'
}
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer'
]
REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'

# AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)
