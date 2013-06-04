# -*- coding: utf-8 -*-

from .helpers import {{ project_name }}TestCase
from django.conf import settings


class TestTestCase({{ project_name }}TestCase):
    def test_settings_is_testing(self):
        self.assertTrue(settings.IS_TESTING)
