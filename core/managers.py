from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    USER = "user", _('пользователь')
    ADMIN = "admin", _('администратор')


class UserManager(BaseUserManager):
    """
    определяем метод создания пользователя через manage.py createsuperuser
    """

    def create_user(self, username, email, first_name=None, last_name=None, password=None, role=UserRoles.USER):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            role=role
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        """
        функция для создания суперпользователя — создаем админинстратора
        """

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            role=UserRoles.ADMIN
        )
        # user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
