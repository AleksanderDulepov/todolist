from django.db.models import Q
from rest_framework import serializers
from core.serializers import UserProfileSerializer
from goals.models import Goal, BoardParticipant


class GoalCreateSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Goal object when creating"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if not BoardParticipant.objects.filter(
                Q(role=BoardParticipant.Role.owner) | Q(role=BoardParticipant.Role.writer), board=value.board,
                user=self.context['request'].user).exists():
            raise serializers.ValidationError("not writer/owner this board")

        return value

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Goal objects in other cases"""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
