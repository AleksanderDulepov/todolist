
from tests.factories import UserFactory
from pytest_factoryboy import register

pytest_plugins="tests.fixtures"

register(UserFactory)


