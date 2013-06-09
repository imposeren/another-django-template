# Put apps and their settings here

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
]


COMPRESS_ENABLED = False  # Compression is not tested!
