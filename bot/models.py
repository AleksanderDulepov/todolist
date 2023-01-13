from django.db import models

from core.models import User


class State(models.IntegerChoices):
    first_visit = 0, "Первый визит"
    not_authorized = 1, "Еще не авторизованный"
    authorized = 2, "Авторизованный"
    input_category = 3, "Выбор категории"
    input_title_goal = 4, "Ввод названия цели"


class TgUser(models.Model):
    """
    Класс для представления обьекта пользователя, обратившегося к телеграм-боту

    Атрибуты
    --------
    t_chat_id: int
    	идентификатор чата в телеграм
    t_user_id: int
    	идентификатор пользователя в телеграм
    fk_user: User
    	связанный обьект пользователя из базы данных web-приложения
    verification_code: str
    	код для регистрации пользователя в телеграмм боте через web-приложение
    """

    class Meta:
        verbose_name = "Пользователь в ТГ"

    t_chat_id = models.CharField(max_length=255)
    t_user_id = models.CharField(max_length=255)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=255, null=True, blank=True)
    state = models.IntegerField(verbose_name="Состояние", choices=State.choices, default=State.first_visit)
