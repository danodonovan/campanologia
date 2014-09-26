#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os

BASE_DIR = \
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                __file__
            )
        )
    )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PSQL_DB_NAME'),
        'USER': os.getenv('PSQL_DB_USER'),
        'PASSWORD': os.getenv('PSQL_DB_PASS'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_ROOT = '/var/www/methodringing-static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bells', 'static_files'),
)

ALLOWED_HOSTS = [
    'localhost',
    '178.62.38.10',
    '.methodringing.co.uk',
    '.ringingmethods.co.uk'
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Local memory caching is default if unspecified, but let's specify anyway
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': os.getenv('LOCMEM_LOCATION')
    }
}

# search using whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': '/var/www/whoosh_index',
    },
}
