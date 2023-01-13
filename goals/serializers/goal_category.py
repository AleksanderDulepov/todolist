from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.serializers import UserProfileSerializer
from goals.models import GoalCategory, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of GoalCategory object when creating"""

    # автопростановка текущего юзера self.request.user при создании обьекта
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # получение обьекта доски через pk
    board = serializers.SlugRelatedField(required=True, queryset=Board.objects.all(), slug_field="pk")

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "board")
        fields = "__all__"

    def create(self, validated_data):
        owner = validated_data['user']
        board = validated_data['board']

        if BoardParticipant.objects.filter(Q(role=BoardParticipant.Role.owner) |
                                           Q(role=BoardParticipant.Role.writer), board=board,
                                           user=owner
                                           ).exists():
            goal_category = GoalCategory.objects.create(**validated_data)
        else:
            raise PermissionDenied("You don't have permission to create goal category with this board")
        return goal_category


class GoalCategorySerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of GoalCategory objects in other cases"""

    # для вывода требуемых полей userа и без возможности перезаписи
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")