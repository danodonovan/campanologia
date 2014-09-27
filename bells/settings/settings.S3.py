#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os

# Access information for the S3 bucket
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME

# Static files are stored in the bucket at /static
# and user-uploaded files are stored at /media
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = 'media'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = 'static'
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

# Construct the paths to resources on S3 via
# the bucket name and the necessary paths
MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = '//%s.s3.amazonaws.com/%s/' % \
            (AWS_STORAGE_BUCKET_NAME, DEFAULT_S3_PATH)
STATIC_ROOT = '/%s/' % STATIC_S3_PATH
STATIC_URL = '//%s.s3.amazonaws.com/%s/' % \
             (AWS_STORAGE_BUCKET_NAME, STATIC_S3_PATH)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'