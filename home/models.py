from __future__ import absolute_import, unicode_literals

from pages.models import Page


class HomePage(Page):
    is_creatable = False
    default_slug = 'home'
