# -*- coding: utf-8 -*-
"""Django settings for project_name project.
this settings are stored in repository so please do not add settings for
*local* env to files in this package. To create local settings:

1. create some file `mysettings.py` and import this package::

      from project_name.settings import *

2. override whatever settings you want

3. to start project with your settings use environment variable::

      DJANGO_SETTINGS_MODULE=mysettings django-admin.py runserver

You can use example settings from `local_settings` folder::

   cp local_settings/my_default.py local_settings/my.py
   DJANGO_SETTINGS_MODULE=local_settings.my


To create deault settings for any environment edit some file in this package
(`project_name.settings`)

To add default settings for dev/prod/staging environments, please edit
`local_settings/YOUR_ENV_NAME.py`

"""

from .default_django import *
from .apps import *
from .project_specific import *
