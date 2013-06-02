# -*- coding: utf-8 -*-
import autocomplete_light
from django.contrib.auth.models import User


autocomplete_light.register(
    User,
    search_fields=['username', 'email', 'first_name', 'last_name'],
)
