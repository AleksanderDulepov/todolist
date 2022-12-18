import pytest

from tests.factories import UserFactory
from pytest_factoryboy import register

from todolist import settings

pytest_plugins="tests.fixtures"

register(UserFactory)

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default']={'ENGINE': 'django.db.backends.sqlite3',
#                                    'NAME': settings.BASE_DIR / 'db.sqlite3',}

