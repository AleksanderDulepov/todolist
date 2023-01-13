from django.db.models import Q
from rest_framework import serializers
from core.serializers import UserProfileSerializer
from goals.models import GoalComment, BoardParticipant

class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of GoalComment object when creating"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_goal(self, value):
        if not BoardParticipant.objects.filter(
                Q(role=BoardParticipant.Role.owner) | Q(role=BoardParticipant.Role.writer),
                board=value.category.board, user=self.context['request'].user).exists():
            raise serializers.ValidationError("not writer/owner this board")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of GoalComment objects in other cases"""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"