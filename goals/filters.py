import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal, GoalComment, GoalCategory


class GoalDateFilter(rest_framework.FilterSet):
    """А сlass that extends FilterSet to manage filtering Goal objects"""

    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"), #первое по умолчанию: ?priority=1, второе при передаче lookup: ?priority__in
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class CommentFilter(rest_framework.FilterSet):
    """А сlass that extends FilterSet to manage filtering GoalComment objects"""

    goal = django_filters.CharFilter(field_name="goal__id", lookup_expr="exact")

    class Meta:
        model = GoalComment
        fields = ["goal"]


class BoardFilter(rest_framework.FilterSet):
    """А сlass that extends FilterSet to manage filtering Board objects"""

    board = django_filters.CharFilter(field_name="board__id", lookup_expr="exact")

    class Meta:
        model = GoalCategory
        fields = ["board"]

