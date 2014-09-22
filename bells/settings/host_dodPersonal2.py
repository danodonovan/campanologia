#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.postgresql_psycopg2',
        'NAME': os.getenv('PSQL_DB_NAME'),
        'USER': os.getenv('PSQL_DB_USER'),
        'PASSWORD': os.getenv('PSQL_DB_PASS')
    }
}

STATIC_ROOT = '/var/www/methodringing/static'
STATIC_URL = '/static/'
