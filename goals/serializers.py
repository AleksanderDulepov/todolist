from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import UserProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
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
    # для вывода требуемых полей userа и без возможности перезаписи
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


# -----------------------
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# -----------------------

class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    # для вывода требуемых полей userа и без возможности перезаписи
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


class BoardCreateSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Board
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(required=True, queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = BoardParticipant
        read_only_fields = ("id", "created", "updated", "board")
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(required=True)

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = '__all__'

    # если пондобится дозапись, а не перезапись-править метод
    def update(self, instance, validated_data):
        print(validated_data)
        owner = validated_data.pop('user')
        participants_new_arr = validated_data.pop('participants')
        participants_new_dict = {
            part['user'].id: part for part in participants_new_arr if part['user'].username != owner.username
        }
        participants_old_arr = instance.participants.exclude(user=owner).all()

        with transaction.atomic():
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
