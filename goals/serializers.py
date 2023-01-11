from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import UserProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


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


# -----------------------
class GoalCreateSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Goal object when creating"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        # if value.user != self.context["request"].user:
        #     raise serializers.ValidationError("not owner of category")

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


# -----------------------

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

    # для вывода требуемых полей userа и без возможности перезаписи
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


class BoardCreateSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Board object when creating"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(board=board, user=user, role=BoardParticipant.Role.owner)
        return board


class BoardListSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Board objects when outputing list"""

    class Meta:
        model = Board
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of BoardParticipant objects"""

    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(required=True, queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = BoardParticipant
        read_only_fields = ("id", "created", "updated", "board")
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    """А сlass that manages the serialization of Board objects in other cases"""

    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(required=True)

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = '__all__'

    def update(self, instance, validated_data):
        owner = self.context['request'].user
        participants_new_arr = validated_data.pop('participants')
        participants_new_dict = {part['user'].id: part for part in participants_new_arr if
                                 part['user'].username != owner.username}
        participants_old_arr = instance.participants.exclude(user=owner)
        participants_old_dict = {part.user.id: part for part in participants_old_arr}

        new_dict_after_checking = []

        with transaction.atomic():
            if self.partial:
                # patch
                for new_part in participants_new_dict:
                    if new_part in participants_old_dict.keys():
                        new_role = participants_new_dict[new_part]['role']
                        matched_user = participants_new_dict[new_part]['user']
                        old_role = participants_old_dict[new_part].role
                        if new_role != old_role:
                            board_part = BoardParticipant.objects.get(board=instance, user=matched_user)
                            board_part.role = new_role
                            board_part.save()
                    else:
                        new_dict_after_checking.append(participants_new_dict[new_part])

                for new_part in new_dict_after_checking:
                    BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])

            else:
                # put
                for old_part in participants_old_arr:
                    if old_part.user.id not in participants_new_dict:
                        old_part.delete()
                    else:
                        if old_part.role != participants_new_dict[old_part.user.id]["role"]:
                            old_part.role = participants_new_dict[old_part.user.id]["role"]
                            old_part.save()
                        del participants_new_dict[old_part.user.id]

                for new_part in participants_new_dict.values():
                    BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])

            instance.title = validated_data['title']
            instance.save()

        return instance
