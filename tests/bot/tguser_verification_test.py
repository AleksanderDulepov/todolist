import pytest

from bot.models import State
from bot.serializers import BotVerifySerializer


@pytest.mark.django_db
def test_tguser_verification(client, user, tg_user, authorized_user_cookie):
    data = {"verification_code": "1q2w3e4r5t6y7u8"}

    BotVerifySerializer.is_test=True

    expected_response = {"t_chat_id": "1",
                         "t_user_id": "1",
                         "fk_user": 1,
                         "verification_code": "1q2w3e4r5t6y7u8",
                         "state": State.authorized
                         }

    response = client.patch("/bot/verify", data, content_type="application/json")
    BotVerifySerializer.is_test = False

    assert response.status_code == 200
    assert response.data == expected_response
