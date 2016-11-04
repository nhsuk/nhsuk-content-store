from __future__ import absolute_import, unicode_literals

from .base import *  # noqa

DEBUG = False

try:
    from .local import *  # noqa
except ImportError:
    pass
