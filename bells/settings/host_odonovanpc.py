#! /usr/bin/env python
import os

SECRET_KEY = "this is not a secret key"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'methods.sqlite3'),
    }
}

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    #os.path.abspath(os.path.join('..', 'bootstrap')),
    os.path.abspath(os.path.join('bells', 'static_files')),
)

TEMPLATE_DIRS = (os.path.abspath('templates'), )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    ## where messages are to be passed to
    'loggers': {
        'django_info': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django_debug': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django_null': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    ## determine what happens to each message in a logger
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    ## perform additional filtering on messages if needed (it is not)
    'filters': {},
    ## format the output text
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'debug': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    }
}
