from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import ModelSerializer


class UserCreateView(CreateAPIView):
	queryset=User.objects.all()
	serializer_class=ModelSerializer
