import json

import django.core.exceptions
import rest_framework.exceptions
from django.core.exceptions import ValidationError, BadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
	UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer, UserUpdatePassword


class UserCreateView(CreateAPIView):
	queryset=User.objects.all()
	serializer_class=UserSignupSerializer


class UserLoginView(CreateAPIView):
	queryset=User.objects.all()
	serializer_class=UserLoginSerializer

	def post(self, request, *args, **kwargs):
		username=request.data.get('username')
		password=request.data.get('password')

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

	#проверка переданных данных и получение обьекта пользователя
		user = authenticate(request, username=username, password=password)
		if user is not None:
			#"запоминание" сессии пользователя в куки
			login(request, user)
			return JsonResponse({"username":username,
								 "first_name":user.first_name,
								 "last_name":user.last_name,
								 "email":user.email},
								status=200)
		else:
			raise ValidationError("Wrong values")

class UserProfileView(RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticated]
	# authentication_classes = [AuthenticationWithoutCSRF]

	#доступ к текущему пользователю через куки, а не через lookup
	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, id=self.request.user.id)
		return obj

	def put(self, request, *args, **kwargs):
		return super().patch(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		logout(request)
		return HttpResponse(status=204)


class UserUpdatePasswordView(UpdateAPIView):
	queryset=User.objects.all()
	serializer_class=UserUpdatePassword
	permission_classes=[IsAuthenticated]


	# доступ к текущему пользователю через куки, а не через lookup
	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, id=self.request.user.id)
		return obj

	def patch(self, request, *args, **kwargs):
		user = self.get_object()
		old_password = request.data.get('old_password')
		new_password = request.data.get('new_password')

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		if not user.check_password(old_password):
			raise serializers.ValidationError({"old_password":"Wrong value"})

		try:
			validate_password(new_password)
		except ValidationError as error:
			raise serializers.ValidationError({"new_password": error.messages})

		user.set_password(new_password)
		user.save()

		return JsonResponse({"old_password":old_password, "new_password":new_password},status=200)

	# def patch(self, request, *args, **kwargs):
	# 	user = self.get_object()
	# 	old_password = request.data.get('old_password')
	# 	new_password = request.data.get('new_password')
	# 	if not old_password:
	# 		raise serializers.ValidationError({"old_password":"This field id required"})
	# 	if not new_password:
	# 		raise serializers.ValidationError({"new_password":"This field id required"})
	#
	# 	if not user.check_password(old_password):
	# 		raise serializers.ValidationError({"old_password":"Wrong value"})
	#
	# 	try:
	# 		validate_password(new_password)
	# 	except ValidationError as error:
	# 		raise serializers.ValidationError({"new_password": error.messages})
	#
	# 	user.set_password(new_password)
	# 	user.save()
	#
	# 	return JsonResponse({"old_password":old_password, "new_password":new_password},status=200)

	def put(self, request, *args, **kwargs):
		return self.patch(request, *args, **kwargs)