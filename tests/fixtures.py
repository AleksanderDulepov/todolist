import json

import pytest


@pytest.fixture
@pytest.mark.django_db
def authorized_user_cookie(client, user):
    user = user
    user.save()

    response = client.post("/core/login",
                           {"username": user.username, "password": "test_password0"},
                           content_type="application/json",
                           )
    # извлекаем весь обьект cookies.SimpleCookie по ключу sessionid из словаря response.cookies
    return response.cookies['sessionid']
