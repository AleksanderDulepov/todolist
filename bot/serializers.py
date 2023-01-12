from django.db import transaction
from rest_framework import serializers

from bot.models import TgUser, State
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class BotVerifySerializer(serializers.ModelSerializer):
    """A class that manages the serialization of TgUser object when updating"""

    verification_code=serializers.CharField(max_length=15, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_test=False

    class Meta:
        model = TgUser
        # fields = "__all__"
        exclude = ["id"]

    def update(self, instance, validated_data):
        owner = self.context['request'].user
        with transaction.atomic():
            instance.fk_user=owner
            instance.state = State.authorized
            instance.save()

            self.send_ok_verification(chat_id=instance.t_chat_id)

            return instance

    def send_ok_verification(self, chat_id: str):
        if not self.is_test:
            tg_client = TgClient(TG_TOKEN)
            tg_client.send_message(chat_id=chat_id, text="[verification has been completed]")

