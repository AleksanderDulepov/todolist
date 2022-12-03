from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from core.models import User
from core.serializers import UserCreateSerializer


class UserViewSet(ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserCreateSerializer
