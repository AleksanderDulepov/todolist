import json

import pytest

from goals.serializers import GoalCommentSerializer


@pytest.mark.django_db
def test_goal_comment_create(client, authorized_user_cookie, goal_first):
    data = {
        "text": "test_text_goal",
        "goal": goal_first.id
    }
    expected_response = data

    response = client.post("/goals/goal_comment/create", data, content_type="application/json")

    assert response.status_code == 201

    try:
        del response.data["id"]
        del response.data["created"]
        del response.data["updated"]
    except Exception as e:
        raise AssertionError("Wrong response data structure")

    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_comment_list(client, authorized_user_cookie, goal_comment_first):
    expected_response = GoalCommentSerializer(goal_comment_first).data

    response = client.get("/goals/goal_comment/list")

    assert response.status_code == 200
    assert json.loads(response.content)[0] == json.loads(json.dumps((expected_response)))


@pytest.mark.django_db
def test_goal_comment_retrieve(client, authorized_user_cookie, goal_comment_first):
    expected_response = GoalCommentSerializer(goal_comment_first).data

    response = client.get(f"/goals/goal_comment/{goal_comment_first.id}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_comment_update(client, authorized_user_cookie, goal_comment_first):
    data = {"text": "updated_text"}

    expected_response = data["text"]

    response = client.put(f"/goals/goal_comment/{goal_comment_first.id}", data, content_type="application/json")

    assert response.status_code == 200
    assert response.data.get("text") == expected_response


@pytest.mark.django_db
def test_goal_comment_delete(client, authorized_user_cookie, goal_comment_first):
    response = client.delete(f"/goals/goal_comment/{goal_comment_first.id}")
    assert response.status_code == 204

# с контролем пермишеннов

@pytest.mark.django_db
def test_goal_comment_create_fail(client, authorized_user_cookie, goal_second):
    data = {
        "text": "test_text_goal",
        "goal": goal_second.id
    }
    response = client.post("/goals/goal_comment/create", data, content_type="application/json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_goal_comment_retrieve_fail(client, authorized_user_cookie, goal_comment_second):
    response = client.get(f"/goals/goal_comment/{goal_comment_second.id}")
    assert response.status_code == 403

@pytest.mark.django_db
def test_goal_comment_update_fail(client, authorized_user_cookie, goal_comment_second):
    data = {"text": "updated_text"}
    response = client.put(f"/goals/goal_comment/{goal_comment_second.id}", data, content_type="application/json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_goal_comment_delete_fail(client, authorized_user_cookie, goal_comment_second):
    response = client.delete(f"/goals/goal_comment/{goal_comment_second.id}")
    assert response.status_code == 403