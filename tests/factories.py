import factory
from factory import PostGenerationMethodCall

import goals
from core.models import User
from goals.models import GoalCategory, Board


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_username"
    first_name = "test_first_name"
    last_name = "test_last_name"
    email = "test@email.com"
    is_superuser = True

    password = PostGenerationMethodCall('set_password',
                                        'test_password0')


class BoardFirstFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title='board_title_1'
    is_deleted=False


class UserSecondFactory(UserFactory):
    class Meta:
        model = User

    username = "test_username_second"

class BoardSecondFactory(BoardFirstFactory):
    title = "title_board_2"




