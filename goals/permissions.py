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
        global message
        if obj.isinstance(GoalCategory):
            obj = obj.board
        if obj.isinstance(Goal):
            obj = obj.category.board
        if obj.isinstance(GoalComment):
            obj = obj.goal.category.board

        if request.method in permissions.SAFE_METHODS:
            message = "You don't have permission because board doesn't include you"
            return BoardParticipant.objects.filter(board=obj, user=request.user).exists()
        else:
            message = "You don't have permission because your role is not owner/writer"
            return BoardParticipant.objects.filter(Q(role=BoardParticipant.Role.owner) |
                                                   Q(role=BoardParticipant.Role.writer),
                                                   board=obj,
                                                   user=request.user).exists()
