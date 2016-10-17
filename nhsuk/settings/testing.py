from .dev import *  # noqa


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


MIGRATION_MODULES = DisableMigrations()

TEST_RUNNER = 'core.testing.runner.CustomTestSuiteRunner'
