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

    # other
    'south',
    'django_nose',
    # 'userena',
    # 'guardian',
    # 'easy_thumbnails',

    # project
    'apps.core',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
