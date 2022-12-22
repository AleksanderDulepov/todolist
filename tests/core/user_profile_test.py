import pytest

@pytest.mark.django_db
def test_user_get_profile(client, user, authorized_user_cookie):
    expected_response = {"id": user.id,
                         "username": user.username,
                         "first_name": user.first_name,
                         "last_name": user.last_name,
                         "email": user.email}

    #добавляем в запрос обьект cookies.SimpleCookie из фикстуры
    #в целом принудительно передавать куки не обязательно, так как куки от authorized_user уже есть в client.cookies
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
