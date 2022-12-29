from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import BoardFilter
from goals.models import GoalCategory, Board
from goals.permissions import GoalsBoardPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    ordering_fields = ["title", "created"]  # указание, по каким полям может выполняться сортировка через ?ordering=...
    ordering = ["title"]  # сортировка по умолчанию (когда не передан ?ordering=...)
    search_fields = ["title"]  # для поиска через get параметр ?search=...
    filterset_class = BoardFilter

    # получение списка текущего авторизованного пользователя
    def get_queryset(self):
        return GoalCategory.objects.select_related("user", "board").filter(
            Q(user=self.request.user) & Q(is_deleted=False) |
            (Q(board__participants__user=self.request.user) & Q(board__is_deleted=False)))


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes=[IsAuthenticated, GoalsBoardPermissions]

    def get_queryset(self):
        #чтобы не возникала 404 когда передана чужая категория (будет 403 от пермишена) - иначе like GoalCategoryListView
        return GoalCategory.objects.all()

    # без удаления обьекта из базы-только проставление is_deleted = True
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
