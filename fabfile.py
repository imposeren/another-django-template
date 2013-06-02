# -*- coding: utf-8 -*-
"""
To init project with virtualenv in project dir (.env)::

    fab initenv initproject

To init project with env that uses virtualenvwrapper::

    fab use_env_wrapper env_name:project_name_env initenv

To run other commands with customized env::

    fab use_env_wrapper env_name:project_name_env {{ command }}
    # or
    fab env_name:my_env_dir {{ command }}
    # or with default env in ./.env/
    fab {{ command }}


You can specify global settings in ~/.fabricrc::

   use_env_wrapper=yes
   virtual_env_name=myproject_env

after this you can run fab commands withoud specifying args: `use_env_wrapper` and `env_name`

"""

from distutils.util import strtobool
from functools import wraps

from fabric.api import env,  lcd, local, prefix, settings
from fabric.contrib.console import confirm
from fabric.utils import puts


env.use_env_wrapper = strtobool(getattr(env, 'use_env_wrapper', '.no'))
env.virtual_env_name = getattr(env, 'virtual_env_name', '.env')
if env.use_env_wrapper:
    env.virtual_env_name = 'project_name_env'

env.active_prefixes = ('', '')


def test():
    activate_virtualenv()
    local("./manage.py test project_name")


def env_name(virtual_env_name):
    env.virtual_env_name = virtual_env_name


def use_env_wrapper():
    env.use_env_wrapper = True


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
    activate_virtualenv()
    prefixed(local)('pip install -r requirements.txt')


def activate_virtualenv():
    if not env.use_env_wrapper:
        env.active_prefixes = ('source %s/bin/activate' % env.virtual_env_name, 'true')
    else:
        env.active_prefixes = ('source `which virtualenvwrapper.sh`', 'workon %s' % env.virtual_env_name)


def prefixed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with prefix(env.active_prefixes[0]), prefix(env.active_prefixes[1]):
            func(*args, **kwargs)
    return wrapper


@prefixed
def init_project():
    activate_virtualenv()
    with lcd('local_settings'):
        local("cp custom_default.py custom.py")
    if confirm("Please edit local_settings/custom.py. Continue init (you may continue it later)?"):
        postinit()
    else:
        puts("You can continue init with `fab postinit`")


@prefixed
def post_init():
    activate_virtualenv()
    local("./manage.py syncdb")


def local_fab_settings():
    puts('use wrapper: %(use_env_wrapper)s\nenv_name: %(virtual_env_name)s' % env)
