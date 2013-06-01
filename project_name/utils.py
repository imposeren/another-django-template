# -*- coding: utf-8 -*-
# Put non django related utils here

import os

path_from_utils_root = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

PROJECT_ROOT = path_from_utils_root(os.pardir)

path_in_project = lambda *x: os.path.abspath(os.path.join(PROJECT_ROOT, *x))
