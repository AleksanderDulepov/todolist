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
                         # "password": "hz",
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