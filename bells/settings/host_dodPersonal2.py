#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os

BASE_DIR = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )

DEBUG = False
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
    # os.path.abspath(os.path.join('..', 'bootstrap')),
    os.path.join(BASE_DIR, 'bells', 'static_files'),
)

assert os.path.isdir(STATICFILES_DIRS[0]), "not a real dir"

ALLOWED_HOSTS = [
    'localhost',
    '178.62.38.10'
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


