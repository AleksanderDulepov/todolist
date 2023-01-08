from django.db import transaction
from rest_framework import serializers

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class BotVerifySerializer(serializers.ModelSerializer):
    verification_code=serializers.CharField(max_length=15, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        fields = "__all__"
        read_only_fields = ("id", "t_chat_id", "t_user_id", "verification_code")

    def update(self, instance, validated_data):
        owner = self.context['request'].user
        with transaction.atomic():
            instance.fk_user_id=owner.id
            instance.save()

            tg_client = TgClient(TG_TOKEN)
            tg_client.send_message(chat_id=instance.t_chat_id, text="[verification has been completed]")

        return instance
