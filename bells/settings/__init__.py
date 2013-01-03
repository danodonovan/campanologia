# Django settings for bells_dj project.
import os; os.environ['LANG'] = 'en_US.UTF-8' # PyCharm ignores environment
# for site specific settings
import socket
HOSTNAME = socket.gethostname().lower().split('.')[0].replace('-','')
# HOSTNAME example odonovan-pc becomes odonovanpc

# general settings
ADMINS = (
    ("Dan O'Donovan", 'web.dan.odonovan@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-GB'
USE_I18N = False
USE_L10N = False
USE_TZ = False
MEDIA_ROOT = ''
MEDIA_URL = ''

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import method from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DEBUG = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'bells.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bells.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'methods',
)


## host specific settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = None

SITE_ID = 1

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = None

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = None

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    None,
)

TEMPLATE_DIRS = (None,)

LOGGING = None

# import the host specific settings
try:
    exec "from bells.settings.host_%s import *" % HOSTNAME
except ImportError:
    pass

# Pull in the local changes - these are not checked into VCS
try:
    from bells.settings.local import *
except ImportError:
    pass
