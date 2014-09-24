#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os

BASE_DIR = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )

#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

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

STATIC_ROOT = '/opt/venv/static'
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['localhost', ]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
