# -*- coding: utf-8 -*-

from django.contrib import admin

import autocomplete_light

from .models import AdminAutocompleteDemo


class AdminAutocompleteDemoAdmin(admin.ModelAdmin):
    # This will generate a ModelForm that has user autocompletion
    form = autocomplete_light.modelform_factory(AdminAutocompleteDemo)

admin.site.register(AdminAutocompleteDemo, AdminAutocompleteDemoAdmin)
