from django.http import JsonResponse
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import Board, Goal
from goals.permissions import BoardPermissions
from goals.serializers import BoardCreateSerializer, BoardListSerializer, BoardSerializer


class BoardCreateView(CreateAPIView):
	model=Board
	permission_classes=[IsAuthenticated]
	serializer_class=BoardCreateSerializer


class BoardListView(ListAPIView):
	permission_classes=[IsAuthenticated]
	serializer_class=BoardListSerializer
	pagination_class = LimitOffsetPagination
	filter_backends=[filters.OrderingFilter]
	ordering_fields=['title']
	ordering=['-created']

	#все доски, где юзер является участником
	def get_queryset(self):
		# доступ к связанному обьекту через related_name модели BoardParticipant
		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

class BoardView(RetrieveUpdateDestroyAPIView):
	model=Board
	permission_classes=[IsAuthenticated, BoardPermissions]
	serializer_class=BoardSerializer

	#все доски, где юзер является участником
	def get_queryset(self):
		# доступ к связанному обьекту через related_name модели BoardParticipant
		return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

	# def patch(self, request, *args, **kwargs):
	# 	serializer=self.get_serializer(Board.objects.get(pk=kwargs.get('pk')),data=request.data, partial=True)
	# 	if serializer.is_valid():
	# 		serializer.save
	# 		return JsonResponse(status=201, data=serializer.data)

	def perform_destroy(self, instance):
		instance.is_deleted=True
		instance.save()
		instance.categories.update(is_deleted=True)
		Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
		#добавить удаление обьектов BoardParticipant после удаление доски

		return instance