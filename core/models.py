from django.contrib.auth.models import AbstractUser
from django.db import models
from core.managers import UserManager, UserRoles


class User(AbstractUser):

    def __str__(self):
        return self.username

