import json

import pytest

from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_goal_category_create(client, authorized_user_cookie):
    data = {
        "title": "test_title_goal_category"
    }

    expected_response = data["title"]

    response = client.post("/goals/goal_category/create", data, content_type="application/json")

    assert response.status_code == 201
    assert response.data.get("title") == expected_response


@pytest.mark.django_db
def test_goal_category_list(client, authorized_user_cookie, goal_category):
    expected_response = GoalCategorySerializer(goal_category).data
    response = client.get("/goals/goal_category/list")
    assert response.status_code == 200
    assert json.loads(response.content)[0] == json.loads(json.dumps((expected_response)))


@pytest.mark.django_db
def test_goal_category_retrieve(client, authorized_user_cookie, goal_category):
    expected_response = GoalCategorySerializer(goal_category).data

    response = client.get(f"/goals/goal_category/{goal_category.id}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_category_update(client, authorized_user_cookie, goal_category):
    data = {"title": "updated_title"}

    expected_response = data["title"]

    response = client.put(f"/goals/goal_category/{goal_category.id}", data, content_type="application/json")

    assert response.status_code == 200
    assert response.data.get("title") == expected_response


@pytest.mark.django_db
def test_goal_category_delete(client, authorized_user_cookie, goal_category):
    response = client.delete(f"/goals/goal_category/{goal_category.id}")
    assert response.status_code == 204
