# -*- coding: utf-8 -*-

# django:
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# vendor:
from modelhelpers.mixins import TitleSlugifyMixin, AutoProcessFieldsMixin, get_slugify_mixin
from modelhelpers.utils import unique_slug


class AdminAutocompleteDemo(models.Model):
    user = models.ForeignKey(User)
    data = models.TextField()


class AutoSlugDemo(models.Model, TitleSlugifyMixin):
    """Displays usage of autoslugs. Just add new movie in admin and slug will
    be auto populated

    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        _("Name to be used in urls"), max_length=100, unique=True, blank=True,
        help_text=_("Auto populated"))

    short_description = models.CharField(max_length=100, blank=True, null=True)


class CustomAutoSlugDemo(models.Model, get_slugify_mixin('other_slug', 'custom_name')):
    custom_name = models.CharField(max_length=100, unique=True)
    other_slug = models.SlugField(
        _("Name to be used in urls"), max_length=100, unique=True, blank=True,
        help_text=_("Auto populated"))


class FieldProcessingDemo(models.Model, AutoProcessFieldsMixin):
    SHORT_TEXT_LENGTH = 150
    WORD_DELIMITERS = (u" ", u"," u".")

    creation_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        _("Name to be used in urls"), max_length=100, unique=True, blank=True,
        help_text=_("Auto populated"))

    full_text = models.TextField()
    short_text = models.TextField(blank=True, help_text=_("Auto populated"))

    @classmethod
    def get_short_text(cls, text):
        """ This method calculates short text from `text`. Do not use it directly.
        just access `self.short_text`

        This method is called automatically on save to update `self.short_text`

        """
        shorter = text[:cls.SHORT_TEXT_LENGTH]
        sane_limit = int(cls.SHORT_TEXT_LENGTH / 3)
        for char in cls.WORD_DELIMITERS:
            new_limit = shorter.rfind(char)
            if new_limit >= sane_limit:
                sane_limit = new_limit
        short_text = shorter[:sane_limit]
        if short_text != text:
            short_text = u"%s…" % short_text
        return short_text

    def process_full_text(self, old_value, new_value, changed, *args, **kwargs):
        if changed or not self.pk or not self.short_text:
            self.short_text = FieldProcessingDemo.get_short_text(self.full_text)

    def process_creation_time(self, old_value, new_value, changed, *args, **kwargs):
        if changed or not self.pk or not self.slug:
            if not self.creation_time:
                self.creation_time = timezone.now()
            slug_value = "%s-%s" % (self.creation_time.strftime(u"%Y-%m-%d"), self.title)
            self.slug = unique_slug(FieldProcessingDemo, slug_value)

    def process_title(self, old_value, new_value, changed, old_values):
        old_creation_time = old_values['creation_time']
        if changed and old_creation_time == self.creation_time:
            # force slug recalc only when creation time is not changed
            self.process_creation_time(old_creation_time, self.creation_time, changed, old_values)
