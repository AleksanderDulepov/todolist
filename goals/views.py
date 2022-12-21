from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, pagination, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter, CommentFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering_fields = ["title", "created"]  # указание, по каким полям может выполняться сортировка через ?ordering=...
    ordering = ["title"]  # сортировка по умолчанию (когда не передан ?ordering=...)
    search_fields = ["title"]   #для поиска через get параметр ?search=...

    #получение списка текущего авторизованного пользователя
    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    #без удаления обьекта из базы-только проставление is_deleted = True
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance

#---------------------------
class GoalCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer

class GoalListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    #фильтрация
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    filterset_class = GoalDateFilter
    #поиск
    search_fields = ["title", "description"]

    #получение списка текущего авторизованного пользователя
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

#---------------------------
class GoalCommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView:
    pass


class GoalCommentListView(ListAPIView):
    queryset = GoalComment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend
    ]
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]
    filterset_class = CommentFilter

    # def get_queryset(self):
    #     goal_id = self.request.GET.get('goal', None)
    #     if goal_id:
    #         return self.queryset.filter(goal__id=goal_id)



class GoalCommentView(RetrieveUpdateDestroyAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    permission_classes = [IsAuthenticated]

