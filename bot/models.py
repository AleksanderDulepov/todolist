from django.db import models

from core.models import User


class State(models.IntegerChoices):
    first_visit = 0, "Первый визит"
    not_authorized = 1, "Еще не авторизованный"
    authorized = 2, "Авторизованный"
    input_category = 3, "Выбор категории"
    input_title_goal = 4, "Ввод названия цели"


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь в ТГ"

    t_chat_id = models.CharField(max_length=255)
    t_user_id = models.CharField(max_length=255)
    # fk_user_id=models.CharField(max_length=255, null=True, blank=True)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=255, null=True, blank=True)
    state = models.IntegerField(verbose_name="Состояние", choices=State.choices, default=State.first_visit)