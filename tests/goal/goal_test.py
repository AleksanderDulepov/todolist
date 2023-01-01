import json

import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_goal_create(client, authorized_user_cookie, goal_category):
    data = {
        "title": "test_title_goal",
        "category": goal_category.id,
        "description": "test_description_goal",
        "status": 1,
        "priority": 1,
        "due_date": "2021-12-01"
    }

    expected_response = {
        "title": "test_title_goal",
        "category": goal_category.id,
        "description": "test_description_goal",
        "status": 1,
        "priority": 1,
        "due_date": "2021-12-01T00:00:00Z"
    }

    response = client.post("/goals/goal/create", data, content_type="application/json")

    assert response.status_code == 201

    try:
        del response.data["id"]
        del response.data["created"]
        del response.data["updated"]
    except Exception as e:
        raise AssertionError("Wrong response data structure")

    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_list(client, authorized_user_cookie, goal_first):
    expected_response = GoalSerializer(goal_first).data

    response = client.get("/goals/goal/list")

    assert response.status_code == 200
    assert json.loads(response.content)[0] == json.loads(json.dumps((expected_response)))


@pytest.mark.django_db
def test_goal_retrieve(client, authorized_user_cookie, goal_first):
    expected_response = GoalSerializer(goal_first).data

    response = client.get(f"/goals/goal/{goal_first.id}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_update(client, authorized_user_cookie, goal_first, goal_category):
    data = {"title": "updated_title",
            "category": goal_category.id,
            }

    expected_response_title = data["title"]
    expected_response_category = data["category"]

    response = client.put(f"/goals/goal/{goal_first.id}", data, content_type="application/json")

    assert response.status_code == 200
    assert response.data.get("title") == expected_response_title
    assert response.data.get("category") == expected_response_category


@pytest.mark.django_db
def test_goal_delete(client, authorized_user_cookie, goal_first):
    response = client.delete(f"/goals/goal/{goal_first.id}")
    assert response.status_code == 204

# с контролем пермишеннов

@pytest.mark.django_db
def test_goal_create_fail(client, authorized_user_cookie, goal_category_second):
    data = {
        "title": "test_title_goal",
        "category": goal_category_second.id,
        "description": "test_description_goal",
        "status": 1,
        "priority": 1,
        "due_date": "2021-12-01"
    }

    response = client.post("/goals/goal/create", data, content_type="application/json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_goal_retrieve_fail(client, authorized_user_cookie, goal_second):
    response = client.get(f"/goals/goal/{goal_second.id}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_goal_update_fail(client, authorized_user_cookie, goal_second, goal_category):
    data = {"title": "updated_title",
            "category": goal_category.id,
            }
    response = client.put(f"/goals/goal/{goal_second.id}", data, content_type="application/json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_goal_delete_fail(client, authorized_user_cookie, goal_second):
    response = client.delete(f"/goals/goal/{goal_second.id}")
    assert response.status_code == 403