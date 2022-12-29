from django.db.models import Q
from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(board=obj, user=request.user).exists()
        else:
            return BoardParticipant.objects.filter(board=obj, user=request.user,
                                                   role=BoardParticipant.Role.owner).exists()


class GoalsBoardPermissions(BoardPermissions):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj,GoalCategory):
            obj = obj.board
        if isinstance(obj,Goal):
            obj = obj.category.board
        if isinstance(obj,GoalComment):
            obj = obj.goal.category.board

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(board=obj, user=request.user).exists()
        else:
            return BoardParticipant.objects.filter(Q(role=BoardParticipant.Role.owner) |
                                                   Q(role=BoardParticipant.Role.writer),
                                                   board=obj,
                                                   user=request.user).exists()
