# -*- coding: utf-8 -*-
from annoying.decorators import render_to


@render_to('core/index.html')
def index(request):
    return {}
