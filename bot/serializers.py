from django.db import transaction
from rest_framework import serializers

from bot.models import TgUser, State
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class BotVerifySerializer(serializers.ModelSerializer):
    """A class that manages the serialization of TgUser object when updating"""

    verification_code=serializers.CharField(max_length=15, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        exclude = ["id"]

    def update(self, instance, validated_data):
        owner = self.context['request'].user
        with transaction.atomic():
            instance.fk_user=owner
            instance.state = State.authorized
            instance.save()

            self.send_ok_verification(instance.t_chat_id)

            return instance

    def send_ok_verification(self, chat_id: str):
        tg_client = TgClient(TG_TOKEN)
        tg_client.send_message(chat_id=chat_id, text="[verification has been completed]")

