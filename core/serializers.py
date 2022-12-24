from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError

from core.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password_repeat = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def is_valid(self, raise_exception=False):
        password = self.initial_data.get('password')
        password_repeat = self.initial_data.pop('password_repeat')  # удаляем из данных, чтобы не передавать на запись
        if password != password_repeat:
            raise serializers.ValidationError({"password_repeat": ["Passwords don't match"]})
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})

        hashed_password = make_password(password)
        self.initial_data['password'] = hashed_password  # замена на хешированый, чтобы не переопределять create
        return super().is_valid(raise_exception=raise_exception)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Wrong value"})
        return attrs

    def update(self, instance, validated_data):
        try:
            validate_password(validated_data["new_password"])
        except ValidationError as error:
            raise serializers.ValidationError({"new_password": error.messages})
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
