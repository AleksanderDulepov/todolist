from django.contrib.auth.models import AbstractUser
from django.db import models
from core.managers import UserManager, UserRoles


class User(AbstractUser):
    role = models.CharField(max_length=5, choices=UserRoles.choices, default=UserRoles.USER)
    email = models.EmailField(unique=False, blank=True)

    # переопределение стандартного поведения при сохранении пользоваетелей через createsuperuser
    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # автоматическая простановка is_staff, is_superuser при role=admin на уровне модели
        if self.role == UserRoles.ADMIN:
            self.is_staff = True
            self.is_superuser = True

        super().save(*args, **kwargs)
