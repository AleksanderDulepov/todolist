from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from bot.models import TgUser
from bot.serializers import BotVerifySerializer


class VerifyView(UpdateAPIView):
    serializer_class = BotVerifySerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        try:
            code=self.request.data["verification_code"]
        except:
            raise serializers.ValidationError({"verification_code": ["This field is required"]})

        if TgUser.objects.filter(verification_code=code).exists():
            tg_user_object = TgUser.objects.get(verification_code=code)
        else:
            raise TgUser.DoesNotExist

        return tg_user_object











