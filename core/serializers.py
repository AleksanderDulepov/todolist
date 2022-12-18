from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from core.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    # переопределение методов для валидации и хеширования пароля при записи через  view
    def is_valid(self, raise_exception=False):
        password = self.initial_data.get('password')
        password_repeat = self.initial_data.get('password_repeat')
        if password != password_repeat:
            raise serializers.ValidationError({"password_repeat": ["Passwords don't match"]})
        del self.initial_data['password_repeat']
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    #переопределение только для проверки наличия
    username = serializers.CharField(max_length=128)
    password= serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128,
                                     required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=128, required=True)
    last_name = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)

    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserUpdatePassword(serializers.ModelSerializer):

    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields=["old_password", "new_password"]


