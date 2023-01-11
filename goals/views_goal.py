from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import GoalsBoardPermissions
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    """А сlass that extends CreateAPIView to manage creating Goal object"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """А сlass that extends ListAPIView to get list of Goal objects"""

    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    # фильтрация
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    filterset_class = GoalDateFilter
    # поиск
    search_fields = ["title", "description"]

    # получение списка текущего авторизованного пользователя
    def get_queryset(self):
        # return Goal.objects.filter(user=self.request.user)
        return Goal.objects.select_related('category__board').filter(
            category__board__participants__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    """А сlass that extends RetrieveUpdateDestroyAPIView to manage retrieve, update and destroy Goal object"""

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, GoalsBoardPermissions]

    def get_queryset(self):
        # чтобы не возникала 404 когда передана чужая цель (будет 403 от пермишена)-иначе like GoalListView
        return Goal.objects.all()
