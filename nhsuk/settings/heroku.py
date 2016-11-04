import os

import dj_database_url

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


DATABASES['default'] = dj_database_url.config()  # noqa

ALLOWED_HOSTS = ['.herokuapp.com', 'localhost']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')
IMAGE_SIGNATURE_KEY = os.environ.get('IMAGE_SIGNATURE_KEY', '')

# STATIC FILES / CSS, JS
MIDDLEWARE += [  # noqa
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA AND FILEs / UPLOADED
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', '')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', '')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', '')

MEDIA_URL = "http://%s.blob.core.windows.net/" % (AZURE_ACCOUNT_NAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}
