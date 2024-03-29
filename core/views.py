from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserUpdatePasswordSerializer


class UserCreateView(CreateAPIView):
    """A class that extends CreateAPIView to manage signup of user"""

    queryset = User.objects.all()
    serializer_class = UserSignupSerializer


class UserLoginView(CreateAPIView):
    """A class that extends CreateAPIView to manage login user"""

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return JsonResponse(serializer.data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """A class that extends RetrieveUpdateDestroyAPIView to manage retrieve, update and destroy User object"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    # authentication_classes = [AuthenticationWithoutCSRF]

    # доступ к текущему пользователю через куки, а не через lookup
    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class UserUpdatePasswordView(UpdateAPIView):
    """A class that extends UpdateAPIView to manage updating user's password"""

    queryset = User.objects.all()
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
