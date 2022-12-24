import pytest


@pytest.mark.django_db
def test_user_signup(client):
    data = {"username": "test",
            "password": "Zxcv0804@",
            "password_repeat": "Zxcv0804@",
            "first_name": "test",
            "last_name": "test",
            "email": "test@email.com"}

    expected_response = {"username": "test",
                         "first_name": "test",
                         "last_name": "test",
                         "email": "test@email.com"}

    response = client.post("/core/signup",
                           data,
                           content_type="application/json",
                           )

    del response.data["id"]
    del response.data["password"]

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_signup_fail_password(client):
    data = {"username": "test",
            "password": "Zxcv0804@",
            "password_repeat": "",
            "first_name": "test",
            "last_name": "test",
            "email": "test@email.com"}

    expected_response = {"password_repeat": ["Passwords don't match"]}

    response = client.post("/core/signup",
                           data,
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_signup_fail_username(client, user):
    data = {"username": user.username,
            "password": "Zxcv0804@",
            "password_repeat": "Zxcv0804@",
            "first_name": "test",
            "last_name": "test",
            "email": "test@email.com"}

    expected_response = {"username": ["A user with that username already exists."]}

    response = client.post("/core/signup",
                           data,
                           content_type="application/json",
                           )

    assert response.status_code == 400
    assert response.data == expected_response
