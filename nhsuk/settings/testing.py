from .dev import *  # noqa


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


MIGRATION_MODULES = DisableMigrations()

TEST_RUNNER = 'core.testing.runner.CustomTestSuiteRunner'
FRONTEND_PREVIEW_URL = 'http://example.com/preview/{signature}/{page_id}/{revision_id}'
