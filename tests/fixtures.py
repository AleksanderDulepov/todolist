import pytest


@pytest.fixture
@pytest.mark.django_db
def authorized_user_cookie(client, django_user_model):
    username = "auth_test_username"
    password = "test_password0"
    email = "test@email.com"
    role = "admin"
    is_superuser = True

    user = django_user_model.objects.create_user(username=username, password=password, email=email, role=role,
                                                     is_superuser=is_superuser)

    response = client.post("/core/signup/",
                           {"username": username, "password": password},
                           content_type="application/json",
                           )

    return {"cookie": response.session.session_key, "id_authorized_user": user.id}
