# -*- coding: utf-8 -*-
""" Example local settings. For dev environment::

   from .dev import *

for staging environment::

       from .staging import *

"""
from .dev import *
from {{ project_name }}.utils import path_in_project


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

MEDIA_ROOT = path_in_project('varying', 'uploads')
MEDIA_URL = '/uploads/'

STATIC_ROOT = path_in_project('varying', 'static')
STATIC_URL = '/static/'