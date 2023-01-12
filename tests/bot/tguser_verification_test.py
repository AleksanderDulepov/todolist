import pytest

from bot.models import State


@pytest.mark.django_db
def test_tguser_verification(client, user, tg_user, authorized_user_cookie, monkeypatch):
    data = {"verification_code": "1q2w3e4r5t6y7u8"}

    #подменяем функцию, исключив диалог с ботом
    def mock_send_ok_verification(self, chat_id: str):
        return None
    
    monkeypatch.setattr("bot.serializers.BotVerifySerializer.send_ok_verification", mock_send_ok_verification, raising=True)


    expected_response = {"t_chat_id": "1",
                         "t_user_id": "1",
                         "fk_user": 1,
                         "verification_code": "1q2w3e4r5t6y7u8",
                         "state": State.authorized
                         }

    response = client.patch("/bot/verify", data, content_type="application/json")

    assert response.status_code == 200
    assert response.data == expected_response
