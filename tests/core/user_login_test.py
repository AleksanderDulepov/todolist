import json

import pytest
from requests.cookies import morsel_to_cookie


@pytest.mark.django_db
def test_user_login(client, user, authorized_user_cookie):
    data = {"username": user.username, "password": "test_password0"}

    expected_response = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password
    }

    response = client.post("/core/login",
                           data,
                           content_type="application/json",
                           )

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response
    assert 'sessionid' in response.cookies
    # проверка самого значения sessionid
    assert morsel_to_cookie(response.cookies['sessionid']).value == morsel_to_cookie(authorized_user_cookie).value
