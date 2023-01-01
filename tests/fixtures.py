import json

import pytest

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment


@pytest.fixture
@pytest.mark.django_db
def authorized_user_cookie(client, user):
    user = user
    user.save()

    response = client.post("/core/login",
                           {"username": user.username, "password": "test_password0"},
                           content_type="application/json",
                           )
    # извлекаем весь обьект cookies.SimpleCookie по ключу sessionid из словаря response.cookies
    return response.cookies['sessionid']

#-----------------------boardparts
@pytest.fixture
@pytest.mark.django_db
def bp_first(board_first, user):
    bp_first_object = BoardParticipant.objects.create(role=BoardParticipant.Role.owner, board=board_first, user=user)
    return bp_first_object


@pytest.fixture
@pytest.mark.django_db
def bp_second(board_second, user_second):
    bp_second_object = BoardParticipant.objects.create(role=BoardParticipant.Role.owner, board=board_second,
                                                       user=user_second)
    return bp_second_object

#-----------------------goal_categories
@pytest.fixture
@pytest.mark.django_db
def goal_category(bp_first, user):
    goal_category_object = GoalCategory.objects.create(board=bp_first.board, user=user)
    return goal_category_object

@pytest.fixture
@pytest.mark.django_db
def goal_category_second(bp_second, user_second):
    goal_category_second_object = GoalCategory.objects.create(board=bp_second.board, user=user_second)
    return goal_category_second_object

#-----------------------goals

@pytest.fixture
@pytest.mark.django_db
def goal_first(user, goal_category):
    goal_first_object=Goal.objects.create(user=user, category=goal_category, title="goal_first_title")
    return goal_first_object

@pytest.fixture
@pytest.mark.django_db
def goal_second(user_second, goal_category_second):
    goal_second_object=Goal.objects.create(user=user_second, category=goal_category_second, title="goal_second_title")
    return goal_second_object

#-----------------------goal_comments
@pytest.fixture
@pytest.mark.django_db
def goal_comment_first(user, goal_first):
    goal_comment_first_object=GoalComment.objects.create(goal=goal_first, user=user, text="text_comment_1")
    return goal_comment_first_object

@pytest.fixture
@pytest.mark.django_db
def goal_comment_second(user_second, goal_second):
    goal_comment_second_object=GoalComment.objects.create(goal=goal_second, user=user_second, text="text_comment_2")
    return goal_comment_second_object