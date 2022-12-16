import json

from django.contrib.auth import authenticate, login, logout
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer


class UserCreateView(CreateAPIView):
	queryset=User.objects.all()
	serializer_class=UserSignupSerializer


# class UserLoginView(CreateAPIView):
# 	queryset=User.objects.all()
# 	serializer_class=UserLoginSerializer
#
# 	@method_decorator(csrf_protect)
# 	def post(self, request, *args, **kwargs):
# 		username=request.data.get('username')
# 		password=request.data.get('password')
# 		#проверка переданных данных и получение обьекта пользователя
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			#"запоминание" сессии пользователя в куки (не токен)
# 			login(request, user)
# 			return HttpResponseRedirect('/')
# 		else:
# 			raise PermissionError

@csrf_exempt
def UserLoginView(request):
	if request.method == 'POST':
		data_dict = json.loads(request.body)
		username = data_dict.get('username')
		password = data_dict.get('password')

		print(username, password)
		# аутентификация
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# "запоминание" сессии пользователя в куки (не токен)
			login(request, user)
			return JsonResponse({"username":username,"password":password},status=200)
			# return HttpResponseRedirect('/core/signup')
		else:
			raise PermissionError


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
		return self.update(request, *args, **kwargs)

	# def get(self, request, *args, **kwargs):
	# 	# print(dict(request.session))
	# 	# print(request.session.session_key)
	#
	# 	return super().get(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)


	# def patch(self, request, *args, **kwargs):
	# 	instance = self.get_object()
	# 	serializer = self.get_serializer(instance, data=request.data)
	#
	# 	if serializer.is_valid():
	# 		serializer.save()
	#
	# 	return Response(serializer.data)

	def delete(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/')