import pytest
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_user_get_profile(client, user, authorized_user_cookie):
    expected_response = {"id": user.id,
                         "username": user.username,
                         "first_name": user.first_name,
                         "last_name": user.last_name,
                         "email": user.email}

    # добавляем в запрос обьект cookies.SimpleCookie из фикстуры
    # в целом принудительно передавать куки не обязательно, так как куки от authorized_user уже есть в client.cookies
    response = client.get("/core/profile",
                          cookies=authorized_user_cookie
                          )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_get_profile_fail(client, authorized_user_cookie):
    del client.cookies["sessionid"]
    response = client.get("/core/profile")

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_update(client, authorized_user_cookie, user):
    data = {"username": "updated_username",
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "email": "updatedemail@ys.com"
            }

    expected_response = data
    expected_response["id"] = user.id

    response = client.put("/core/profile", data, content_type="application/json", cookies=authorized_user_cookie)

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_logout(client, authorized_user_cookie):
    response = client.delete("/core/profile", cookies=authorized_user_cookie)

    assert response.status_code == 204
    assert response.cookies != authorized_user_cookie


@pytest.mark.django_db
def test_user_update_password(client, authorized_user_cookie, user):
    data = {"old_password": "test_password0",
            "new_password": "test_new_password0"}

    response = client.put("/core/update_password", data, content_type="application/json",
                          cookies=authorized_user_cookie)

    print(response.data)
    assert response.status_code == 200
    assert response.renderer_context['request'].user.check_password("test_new_password0")
