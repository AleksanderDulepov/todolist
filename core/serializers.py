from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core import exceptions

from core.models import User


class ModelSerializer(serializers.ModelSerializer):

    password_repeat = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['id','username', 'first_name','last_name','email','password','password_repeat']

    #переопределение методов для валидации и хеширования пароля при записи через  view
    def is_valid(self, raise_exception=False):
        password = self.initial_data.get('password')
        password_repeat = self.initial_data.get('password_repeat')
        if password != password_repeat:
            raise ValidationError({"password_repeat":["Passwords don't match"]})
        del self.initial_data['password_repeat']
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().is_valid(raise_exception=raise_exception)



    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user
