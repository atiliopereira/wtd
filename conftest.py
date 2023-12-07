import os
import tempfile

import pytest
from django.conf import settings
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def pytest_configure():
    settings.DEBUG = False
    settings.MEDIA_ROOT = tempfile.mkdtemp(prefix="wrdtest_")
    settings.WHITENOISE_AUTOREFRESH = True
    settings.ALLOWED_HOSTS.extend(
        [
            "another.com",
            "example.com",
        ]
    )
    cache.clear()
