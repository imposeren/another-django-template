# -*- coding: utf-8 -*-

from django.contrib import admin

import autocomplete_light

# project
from project_name.example_app import models


class AdminAutocompleteDemoAdmin(admin.ModelAdmin):
    # This will generate a ModelForm that has user autocompletion
    form = autocomplete_light.modelform_factory(models.AdminAutocompleteDemo)


admin.site.register(models.AdminAutocompleteDemo, AdminAutocompleteDemoAdmin)
admin.site.register(models.AutoSlugDemo, admin.ModelAdmin)
admin.site.register(models.CustomAutoSlugDemo, admin.ModelAdmin)
admin.site.register(models.FieldProcessingDemo, admin.ModelAdmin)