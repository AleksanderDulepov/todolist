from django.db import models
from django.utils import timezone

from core.models import User


class AdstractMixin(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class GoalCategory(AdstractMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(AdstractMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="Описание")
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата выполнения")


class GoalComment(AdstractMixin):
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)
    text = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
