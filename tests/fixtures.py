import json

import pytest


@pytest.fixture
@pytest.mark.django_db
def authorized_user(client, django_user_model):
    username = "auth_test_username"
    password = "test_password0"
    email = "test@email.com"

    user = django_user_model.objects.create_user(username=username, password=password, email=email)
    user.first_name="test"
    user.last_name="test"
    user.save()

    response = client.post("/core/login",
                           {"username": username, "password": password},
                           content_type="application/json",
                           )
    #извлекаем весь обьект cookies.SimpleCookie по ключу sessionid из словаря response.cookies
    return {"cookie": response.cookies['sessionid'], "user": user}
