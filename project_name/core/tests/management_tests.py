# -*- coding: utf-8 -*-

from .helpers import project_nameTestCase
from django.conf import settings


class TestTestCase(project_nameTestCase):
    def test_settings_is_testing(self):
        self.assertTrue(settings.IS_TESTING)
