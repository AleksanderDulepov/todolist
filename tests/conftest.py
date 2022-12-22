from tests.factories import UserFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory
from pytest_factoryboy import register

pytest_plugins="tests.fixtures"

register(UserFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)