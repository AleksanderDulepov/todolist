import json

import pytest
from django.db.models import Q
from django.forms import model_to_dict

from goals.models import Board, BoardParticipant
from goals.serializers import BoardSerializer, BoardListSerializer


@pytest.mark.django_db
def test_board_create(client, authorized_user_cookie, user):
    data = {
        "title": "title"
    }

    expected_response_board = {
        "title": "title",
        "is_deleted": False
    }

    response = client.post("/goals/board/create", data, content_type="application/json")

    assert response.status_code == 201

    try:
        del response.data["id"]
        del response.data["created"]
        del response.data["updated"]
    except Exception as e:
        raise AssertionError("Wrong response data structure")

    assert response.data == expected_response_board

    # проверка автоматического создания BoardParticipant
    board = Board.objects.filter(Q(participants__user=user) & Q(title="title")).first()
    bp = BoardParticipant.objects.filter(user=user, board__title="title", role=BoardParticipant.Role.owner).first()

    bp_dict = model_to_dict(bp, exclude=['id', 'created', 'updated'])

    expected_response_bp = {
        "role": BoardParticipant.Role.owner,
        "user": user.id,
        "board": board.id
    }

    assert bp_dict == expected_response_bp


@pytest.mark.django_db
def test_board_list(client, authorized_user_cookie, bp_first):
    expected_response = BoardListSerializer(bp_first.board).data
    response = client.get("/goals/board/list")
    assert response.status_code == 200
    assert json.loads(response.content)[0] == json.loads(json.dumps((expected_response)))


@pytest.mark.django_db
def test_board_retrieve(client, authorized_user_cookie, bp_first):
    expected_response = BoardSerializer(bp_first.board).data
    response = client.get(f"/goals/board/{bp_first.board.id}")
    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_board_update(client, authorized_user_cookie, bp_first, user):
    data = {"title": "updated_title",
            "participants": [{"role": BoardParticipant.Role.reader, "user": user.username}]}

    expected_response_title = data["title"]
    expected_response_part_role = BoardParticipant.Role.reader
    expected_response_part_user = user.username

    response = client.put(f"/goals/board/{bp_first.board.id}", data, content_type="application/json")

    assert response.status_code == 200
    assert response.data.get("title") == expected_response_title

    for part in response.data.get("participants"):
        if part['role'] == expected_response_part_role and part['user'] == expected_response_part_user:
            return
        else:
            continue
        raise AssertionError("Wrong added user data")


@pytest.mark.django_db
def test_board_delete(client, authorized_user_cookie, bp_first, user):
    response = client.delete(f"/goals/board/{bp_first.board.id}")
    assert response.status_code == 204

    board = Board.objects.filter(Q(participants__user=user) & Q(title=bp_first.board.title)).first()
    assert board.is_deleted == True


# с контролем пермишеннов
@pytest.mark.django_db
def test_board_retrieve_fail(client, authorized_user_cookie, bp_second):
    response = client.get(f"/goals/board/{bp_second.board.id}")
    assert response.status_code == 404


@pytest.mark.django_db
def test_board_retrieve_again(client, bp_second, user_second):
    client.login(username=user_second.username, password="test_password0")
    response = client.get(f"/goals/board/{bp_second.board.id}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_board_update_fail_wrong_user_role(client, authorized_user_cookie, bp_first, user):
    data = {"title": "updated_title",
            "participants": [{"role": BoardParticipant.Role.reader, "user": user.username}]
            }

    expected_response_part_role = BoardParticipant.Role.owner
    response = client.put(f"/goals/board/{bp_first.board.id}", data, content_type="application/json")

    assert response.status_code == 200

    for part in response.data.get("participants"):
        if part['user'] == user.username:
            if part['role'] != expected_response_part_role:
                raise AssertionError("Wrong updated user role")
            else:
                return
        raise AssertionError("Wrong updated user role")


@pytest.mark.django_db
def test_board_update_fail_empty_user(client, authorized_user_cookie, bp_first, user):
    data = {"title": "updated_title",
            "participants": []
            }

    expected_response_part_role = BoardParticipant.Role.owner
    expected_response_part_user = user.username
    response = client.put(f"/goals/board/{bp_first.board.id}", data, content_type="application/json")

    assert response.status_code == 200

    for part in response.data.get("participants"):
        if part['role'] == expected_response_part_role and part['user'] == expected_response_part_user:
            return
        else:
            continue
        raise AssertionError("Wrong updated user data")


@pytest.mark.django_db
def test_board_update_fail_alien_item(client, authorized_user_cookie, bp_second, user_second):
    data = {"title": "updated_title",
            "participants": [{"role": BoardParticipant.Role.reader, "user": user_second.username}]
            }
    response = client.put(f"/goals/board/{bp_second.board.id}", data, content_type="application/json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_board_delete_fail_alien_item(client, authorized_user_cookie, bp_second):
    response = client.delete(f"/goals/board/{bp_second.board.id}")
    assert response.status_code == 404
