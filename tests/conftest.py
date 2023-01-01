
from pytest_factoryboy import register

from tests.factories import UserFactory, UserSecondFactory, BoardFirstFactory, BoardSecondFactory

pytest_plugins="tests.fixtures"

register(UserFactory, "user")
register(UserSecondFactory, "user_second")
register(BoardFirstFactory,"board_first")
register(BoardSecondFactory, "board_second")
