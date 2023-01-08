from django.db import models


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь в ТГ"

    t_chat_id=models.CharField(max_length=255)
    t_user_id=models.CharField(max_length=255)
    fk_user_id=models.CharField(max_length=255, null=True, blank=True)
    verification_code=models.CharField(max_length=255, null=True, blank=True)

