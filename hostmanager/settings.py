#! -*- coding: utf-8 -*-
import os

from manager.settings import *

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATE_FORMAT = 'd E Y'
DATETIME_FORMAT = u'd E Y в H:i'

ADMINS = (
    ('Sergey Levitin', 'selevit@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'hostmanager.db'),
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1

USE_I18N = True
USE_L10N = False
USE_TZ = False

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = COMPRESS_ROOT = os.path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    ('img', os.path.join(STATIC_ROOT, 'img')),
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'you_secret_key'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hostmanager.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hostmanager.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'compressor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'manager',
)

INTERNAL_IPS = ('127.0.0.1',)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'manager.context_processors.auth',
)

NGINX_CONF_TEMPLATE = os.path.join(TEMPLATE_DIRS[0], 'manager/nginx.template.conf')
APACHE_CONF_TEMPLATE = os.path.join(TEMPLATE_DIRS[0], 'manager/apache.template.conf')

HOSTMANAGER_PLACEHOLDER_PATH = os.path.join(TEMPLATE_DIRS[0], 'manager/placeholder.html')
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']

BACKUP_STORAGE_PATH = '/home/web/backup/'
BACKUP_DATABASE_LIST = '/etc/backup/databases'

if os.environ.get('DEVELOPMENT', None):
    from settings_dev import *


