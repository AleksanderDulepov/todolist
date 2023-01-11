from django.db import models
from django.utils import timezone
from core.models import User
from datetime import datetime


class AdstractMixin(models.Model):
    """
    Аn abstract сlass that includes common attributes to be extended by many other models

    Attributes
    --------
    created: datetime.datetime
    	A variable that describes creating date and time
    updated: datetime.datetime
    	A variable that describes updating date and time
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class Board(AdstractMixin):
    """
    А class that includes attributes describe Board model

    Attributes
    --------
    title: str
    	A variable that describes board's title
    is_deleted: bool
    	A variable that includes actual state of board
    """

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"


class BoardParticipant(AdstractMixin):
    """
    А class that includes attributes describe BoardParticipant model

    Attributes
    --------
    board: Board
    	A foreign key that relates BoardParticipant and related Board object
    user: User
    	A foreign key that relates BoardParticipant and related User object
    role: Role
    	A variable that describes object's role
    """

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль",
        choices=Role.choices,
        default=Role.owner
    )


class GoalCategory(AdstractMixin):
    """
    А class that includes attributes describe GoalCategory model

    Attributes
    --------
    board: Board
    	A foreign key that relates GoalCategory and related Board object
    user: User
    	A foreign key that relates GoalCategory and related User object
    title: str
    	A variable that describes category's title
    is_deleted: bool
    	A variable that includes actual state of category
    """

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(AdstractMixin):
    """
    А class that includes attributes describe Goal model

    Attributes
    --------
    user: User
    	A foreign key that relates Goal and related User object
    category: GoalCategory
    	A foreign key that relates Goal and related GoalCategory object
    title: str
    	A variable that describes goal's title
    description: str
    	A variable that describes goal's description
    status:Status
    	A variable that describes goal's status
    priority:Priority
    	A variable that describes goal's priority
    due_date: datetime.datetime
    	A variable that describes deadline to performing the task
    """

    class Meta:
        verbose_name = "Цель"
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

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
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
    """
    А class that includes attributes describe GoalComment model

    Attributes
    --------
    goal: Goal
    	A foreign key that relates GoalComment and related Goal object
    user: User
    	A foreign key that relates GoalComment and related User object
    text: str
    	A variable that describes goal comment's text
    """

    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
