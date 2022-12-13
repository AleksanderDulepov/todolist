from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.models import User


class ModelSerializer(serializers.ModelSerializer):

    password_repeat = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = "__all__"

    #переопределение методов для валидации и хеширования пароля при записи через  view
    def is_valid(self, raise_exception=False):
        password = self.initial_data.get('password')
        password_repeat = self.initial_data.get('password_repeat')
        if password != password_repeat:
            raise ValidationError("Passwords don't match")
        del self.initial_data['password_repeat']
        validate_password(password)
        return super().is_valid(raise_exception=raise_exception)



    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user
