# -*- coding: utf-8 -*-

from django_nose.management.commands.test import Command as TestCommand


class Command(TestCommand):
    def handle(self, *args, **options):
        from django.conf import settings
        settings.IS_TESTING = True
        super(Command, self).handle(*args, **options)
