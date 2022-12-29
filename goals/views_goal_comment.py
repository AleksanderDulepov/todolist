from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import CommentFilter
from goals.models import GoalComment
from goals.permissions import GoalsBoardPermissions
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
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

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board').filter(
            goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes=[IsAuthenticated, GoalsBoardPermissions]

    def get_queryset(self):
        # чтобы не возникала 404 когда передана чужая цель (будет 403 от пермишена)-иначе like GoalCommentListView
        return GoalComment.objects.all()