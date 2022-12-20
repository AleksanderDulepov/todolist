import pytest
from requests import cookies


@pytest.mark.django_db
def test_user_get_profile(client, authorized_user):
    expected_response = {"id": authorized_user['user'].id,
                         "username": authorized_user['user'].username,
                         "first_name": "test",
                         "last_name": "test",
                         "email": authorized_user['user'].email}

    #добавляем в запрос обьект cookies.SimpleCookie из фикстуры
    #в целом принудительно передавать куки не обязательно, так как куки от authorized_user уже есть в client.cookies
    response = client.get("/core/profile",
                      cookies=authorized_user['cookie']
                      )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_get_profile_fail(client, authorized_user):
    del client.cookies["sessionid"]
    response = client.get("/core/profile")

    assert response.status_code == 403
