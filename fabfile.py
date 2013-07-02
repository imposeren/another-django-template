# -*- coding: utf-8 -*-
#{# NOTE: this is django template, so all {{ variables }} will be replaced #}
#{# {% templatetag openvarialbe %} {% templatetag closevarialbe %}  can be used to solve this #}
"""
To init project with virtualenv in project dir (.env)::

    fab autoactivate init_env init_project

To init project with env that uses virtualenvwrapper::

    fab use_env_wrapper env_name:{{ project_name }}_env init_env init_project

To run other commands with customized env::

    fab use_env_wrapper env_name:{{ project_name }}_env COMMAND
    # or
    fab env_name:my_env_dir COMMAND
    # or with default env in ./.env/
    fab autoactivate COMMAND


You can specify global settings in ~/.fabricrc::

   autoactivate=yes
   use_env_wrapper=yes
   virtual_env_name=myproject_env

after this you can run fab commands withoud specifying args: `use_env_wrapper` and `env_name`

You can also set settings in fabsettings.py. Check fabsettings_default.py for example.

"""
import os

from distutils.util import strtobool
from functools import wraps

from fabric.api import env, lcd, local, prefix, settings, abort
from fabric.context_managers import hide
from fabric.contrib.console import confirm
from fabric.utils import puts

__all__ = (
    'env_name', 'use_env_wrapper', 'autoactivate', 'noautoactivate', 'init_env',
    'manage', 'test', 'init_project',
    'syncdb', 'post_init', 'run', 'pip_install', 'update_env',
    'install_reqs', 'migrate', 'schemamigration',
    'generate_template',
)

env.autoactivate = strtobool(getattr(env, 'autoactivate', 'no'))
env.use_env_wrapper = strtobool(getattr(env, 'use_env_wrapper', 'no'))
if env.use_env_wrapper:
    default_env_name = '{{ project_name }}_env'
else:
    default_env_name = '.env'


env.virtual_env_name = getattr(env, 'virtual_env_name', default_env_name)

env.active_prefixes = ('true', 'true')

env.bind_port = getattr(env, 'bind_port', '8000')

env.django_settings = getattr(env, 'django_settings', 'local_settings.custom')

try:
    from fabsettings import *
except ImportError:
    pass

os.environ['DJANGO_SETTINGS_MODULE'] = env.django_settings


def env_name(virtual_env_name):
    """Set name of virtualenv (default: '.env' or '{{ project_name }}_env' if wrapper is used):
    `fab env_name:.my_env args`"""
    env.virtual_env_name = virtual_env_name
    autoactivate()


def use_env_wrapper():
    """Use virtualenvwrapper (default: no): `fab use_env_wrapper args`"""
    env.use_env_wrapper = True
    autoactivate()


def autoactivate():
    """Autoactivate env for each task (default: no) """
    env.autoactivate = True


def noautoactivate():
    env.autoactivate = False


def init_env(requirements='dev'):
    """Init virtualenv and install requirements"""
    if not env.use_env_wrapper:
        with settings(warn_only=True):
            local('rm -rf ./%s' % env.virtual_env_name)
        local('virtualenv %s' % env.virtual_env_name)
    else:
        with prefix('. `which virtualenvwrapper.sh`'):
            with settings(warn_only=True):
                local('rmvirtualenv %s' % env.virtual_env_name)
            local('mkvirtualenv %s' % env.virtual_env_name)
    activate_virtualenv(True)
    prefixed(local)('pip install -r requirements/{0}.txt'.format(requirements))


def _activate_virtualenv():
    if not env.use_env_wrapper:
        env.active_prefixes = ('. %s/bin/activate' % env.virtual_env_name, 'true')
    else:
        env.active_prefixes = ('. `which virtualenvwrapper.sh`', 'workon %s' % env.virtual_env_name)


def activate_virtualenv(force=False):
    if env.autoactivate or force:
        _activate_virtualenv()


def prefixed(func):
    """Activate virtualenv for all calls in decorated function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        activate_virtualenv()
        with prefix(env.active_prefixes[0]), prefix(env.active_prefixes[1]):
            func(*args, **kwargs)
    return wrapper


@prefixed
def manage(command):
    """Run django management commands"""
    local("./manage.py %s" % command)


def test():
    """Run tests. By default tests are run with coverage and it is saved as html
    in ``varying/coverage/index.html``
    """
    manage("test {{ project_name }}")


def init_project():
    """Initialize project for dev environment"""
    with lcd('local_settings'):
        local("cp custom_default.py custom.py")
    if confirm("Please edit local_settings/custom.py. Continue init (you may continue it later)?"):
        post_init()
    else:
        puts("You can continue init with `fab postinit`")


def migrate(param='--no-initial-data'):
    """Update the database"""
    manage("migrate %s" % param)


def schemamigration(app_name=''):
    """Update the database"""
    print green("Migrate apps")
    print "Use migrate:'app_name' to create migration."
    if param:
        manage("schemamigration %s --init" % param)

    manage("migrate --no-initial-data")


def syncdb(noinput=True, no_initial_data=True):
    """Run syncdb"""
    noinput = noinput and '--noinput' or ''
    no_initial_data = no_initial_data and '--no-initial-data' or ''
    manage("syncdb %s %s" % (noinput, no_initial_data))


def post_init():
    """Continue init after settings edited"""
    syncdb()
    migrate(param='')
    # add additional post_init actions here


def run():
    """Run devserver"""
    manage("runserver 0.0.0.0:%s" % env.bind_port)


@prefixed
def pip_install(package):
    """install pacakage with pip"""
    local('pip install %s' % package)


@prefixed
def update_env():
    """Install requirements into env"""
    local('pip install -Ur requirements.txt')


def install_reqs(environ='dev'):
    pip_install('-r requirements/%s.txt' % environ)


def generate_template(project_name='{{ project_name }}'):
    """Generate django project template from "project_name". Warning: original files will be overwritten.
    How it works now:
        all "project_name" strings in *.py files are replaced with "{{ project_name }}"

    """
    data = {'project_name': project_name}
    with settings(warn_only=True), hide('warnings'):
        result = local('grep -qlR "{% templatetag openvariable %} project_name {% templatetag closevariable %}" %(project_name)s local_settings' % data)
    if not result.failed:
        abort('You are trying to generate template from template. '
              'You an startproject from this template and then call this command')

    local('find %(project_name)s local_settings -iname "*.py" -type f -print0 | xargs -0 sed -i "s/%(project_name)s/{% templatetag openvariable %} project_name {% templatetag closevariable %}/g"' % data)
    if project_name != 'project_name':
        local('mv %(project_name)s project_name' % data)

    puts('*.py files in %(project_name)s and local_settings directories are '
         'ready to be used in template project. But fabfile.py is not processed.'
         ' You should use fabfile.py from original template')