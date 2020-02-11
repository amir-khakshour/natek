import os
import django


def pytest_configure(config):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()


def pytest_unconfigure(config):
    # do cleanup
    pass
