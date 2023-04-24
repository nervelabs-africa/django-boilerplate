"""dev.py
settings for dev environments

WARNING: This settings must not be used in production
to use this settings: set your the environment variable ENV=dev
"""
from config.settings.base import *
from django.core.exceptions import *
import environ
import os

ALLOWED_HOSTS = ['*']

# DEV APPS
# NOT ALL LIBRARIES
# HERE MIGHT MAKE IT TO
# STAGING OR PRODUCTION
BETA_APPS = [
    'knox',
    'drf_standardized_errors'
]
INSTALLED_APPS.extend(BETA_APPS)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, '.env-beta')
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

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    #'localhost:3000',
    'http://127.0.0.1:3000',
    #'127.0.0.1:3000'
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.*\.com$",
]

CORS_URLS_REGEX = r'^/api/.*$'

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    'access-control-allow-origin'
]

#CORS_ALLOW_CREDENTIALS = True

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
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'services.authiam.backends.OAuth2ClientCredentialAuthentication',
    ),

    # exception handler
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler'
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

STATIC_URL = '/static/'
BASE_DIR = BASE_DIR.split('/')
BASE_DIR.pop()
BASE_DIR = '/'.join(BASE_DIR)
STATIC_ROOT = BASE_DIR + '/static'
