# Put apps and their settings here

from {{ project_name }}.utils import path_in_project


INSTALLED_APPS = (
    # django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # vendor
    'south',
    'django_nose',
    'compressor',
    'autocomplete_light',

    # project
    '{{ project_name }}.core',
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package={{ project_name }}',
    '--with-progressive',
    '--cover-html',
    '--cover-html-dir="%s"' % path_in_project('varying/coverage/'),
]


COMPRESS_ENABLED = False  # Compression is not tested!
