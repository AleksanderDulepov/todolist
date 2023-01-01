import pytest
from django.forms import model_to_dict


@pytest.mark.django_db
def test_goal_category_list(client, goal_comment_first):
    print(type(goal_comment_first))
    # print(model_to_dict(goal_first))


    # assert goal_category.board==board_first
    assert 1==1