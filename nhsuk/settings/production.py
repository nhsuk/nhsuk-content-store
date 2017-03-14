from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

import os

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*.nhs.uk').split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'nhsuk'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY')
IMAGE_SIGNATURE_KEY = os.environ.get('IMAGE_SIGNATURE_KEY')
PREVIEW_SIGNATURE_KEY = os.environ.get('PREVIEW_SIGNATURE_KEY')

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
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

DEBUG = os.environ.get('DEBUG', '0') == '1'

try:
    from .local import *  # noqa
except ImportError:
    pass
