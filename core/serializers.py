from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from core.models import User


# class UserSignupSerializer(serializers.ModelSerializer):
#     password_repeat = serializers.CharField(max_length=128, required=False)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')
#
#     # переопределение методов для валидации и хеширования пароля при записи через  view
#     def is_valid(self, raise_exception=False):
#         password = self.initial_data.get('password')
#         password_repeat = self.initial_data.get('password_repeat')
#         if password != password_repeat:
#             raise serializers.ValidationError({"password_repeat": ["Passwords don't match"]})
#         del self.initial_data['password_repeat']
#         try:
#             validate_password(password)
#         except ValidationError as e:
#             raise serializers.ValidationError({"password": e.messages})
#         return super().is_valid(raise_exception=raise_exception)
#
#     def create(self, validated_data):
#         user = super().create(validated_data)
#         user.set_password(validated_data["password"])
#         user.save()
#         return user

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




# class UserLoginSerializer(serializers.ModelSerializer):
#     #переопределение только для проверки наличия
#     username = serializers.CharField(max_length=128)
#     password= serializers.CharField(max_length=128)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')

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
        fields = ('username', 'password', 'first_name','last_name','email')


class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=128,
    #                                  required=True,
    #                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # first_name = serializers.CharField(max_length=128, required=True)
    # last_name = serializers.CharField(max_length=128, required=True)
    # email = serializers.EmailField(required=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


# class UserUpdatePassword(serializers.ModelSerializer):
#
#     old_password = serializers.CharField(max_length=255)
#     new_password = serializers.CharField(max_length=255)
#
#     class Meta:
#         model = User
#         fields=("old_password", "new_password")

class UserUpdatePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True, write_only=True)
    new_password=serializers.CharField(required=True, write_only=True)
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        user=attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password":"Wrong value"})
        return attrs

    def update(self, instance, validated_data):
        try:
            validate_password(validated_data["new_password"])
        except ValidationError as error:
            raise serializers.ValidationError({"new_password":error.messages})
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance

