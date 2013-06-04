# -*- coding: utf-8 -*-
from fabric.api import env

env.autoactivate = True
env.bind_port = 8000
env.django_settings = 'local_settings.custom'
