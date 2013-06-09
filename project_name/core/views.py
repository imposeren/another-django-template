# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib import messages


@render_to('core/index.html')
def index(request):
    messages.warning(request, 'This is default {{ project_name }}.core.views.index() view. Pleas override it')
    return {}
