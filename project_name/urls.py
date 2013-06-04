# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

import autocomplete_light


autocomplete_light.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',

    # admin:
    url(r'^admin/', include(admin.site.urls)),

    # vendor:
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # project:
    url(r'^$', '{{ project_name }}.core.views.index', name='index'),

)


if '{{ project_name }}.example_app' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^example/', include('{{ project_name }}.example_app.urls')),
    )
