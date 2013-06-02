# -*- coding: utf-8 -*-
"""
To init project with virtualenv in project dir (.env)::

    fab autoactivate init_env init_project

To init project with env that uses virtualenvwrapper::

    fab use_env_wrapper env_name:project_name_env init_env init_project

To run other commands with customized env::

    fab use_env_wrapper env_name:project_name_env {{ command }}
    # or
    fab env_name:my_env_dir {{ command }}
    # or with default env in ./.env/
    fab autoactivate {{ command }}


You can specify global settings in ~/.fabricrc::

   autoactivate=yes
   use_env_wrapper=yes
   virtual_env_name=myproject_env

after this you can run fab commands withoud specifying args: `use_env_wrapper` and `env_name`

"""

from distutils.util import strtobool
from functools import wraps

from fabric.api import env,  lcd, local, prefix, settings
from fabric.contrib.console import confirm
from fabric.utils import puts


env.autoactivate = strtobool(getattr(env, 'autoactivate', 'no'))
env.use_env_wrapper = strtobool(getattr(env, 'use_env_wrapper', 'no'))
if env.use_env_wrapper:
    default_env_name = 'project_name_env'
else:
    default_env_name = '.env'


env.virtual_env_name = getattr(env, 'virtual_env_name', '.env')

env.active_prefixes = ('true', 'true')


def env_name(virtual_env_name):
    env.virtual_env_name = virtual_env_name
    autoactivate()


def use_env_wrapper():
    env.use_env_wrapper = True
    autoactivate()


def autoactivate():
    env.autoactivate = True


def init_env():
    if not env.use_env_wrapper:
        with settings(warn_only=True):
            local('rm -rf ./%s' % env.virtual_env_name)
        local('virtualenv %s' % env.virtual_env_name)
    else:
        with prefix('source `which virtualenvwrapper.sh`'):
            with settings(warn_only=True):
                local('rmvirtualenv %s' % env.virtual_env_name)
            local('mkvirtualenv %s' % env.virtual_env_name)
    activate_virtualenv(True)
    prefixed(local)('pip install -r requirements.txt')


def _activate_virtualenv():
    if not env.use_env_wrapper:
        env.active_prefixes = ('source %s/bin/activate' % env.virtual_env_name, 'true')
    else:
        env.active_prefixes = ('source `which virtualenvwrapper.sh`', 'workon %s' % env.virtual_env_name)


def activate_virtualenv(force=False):
    if env.autoactivate or force:
        _activate_virtualenv()


def prefixed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        activate_virtualenv()
        with prefix(env.active_prefixes[0]), prefix(env.active_prefixes[1]):
            func(*args, **kwargs)
    return wrapper

@prefixed
def manage(command):
    local("./manage.py %s" % command)


def test():
    manage("test project_name")


@prefixed
def init_project():
    with lcd('local_settings'):
        local("cp custom_default.py custom.py")
    if confirm("Please edit local_settings/custom.py. Continue init (you may continue it later)?"):
        post_init()
    else:
        puts("You can continue init with `fab postinit`")


def syncdb():
    manage("syncdb")


def post_init():
    syncdb()
    # add additional post_init actions here


def run():
    manage("runserver")
