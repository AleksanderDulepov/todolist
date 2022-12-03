from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.managers import UserRoles
from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    #переопределение методов для валидации и хеширования пароля при записи через  view
    def is_valid(self, raise_exception=False):
        password = self.initial_data["password"]
        validate_password(password)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user
