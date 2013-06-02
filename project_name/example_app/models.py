# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class AdminAutocompleteDemo(models.Model):
    user = models.ForeignKey(User)
    data = models.TextField()
