from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import CommentFilter
from goals.models import GoalComment
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


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


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    permission_classes = [IsAuthenticated]
