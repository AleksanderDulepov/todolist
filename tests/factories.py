from factory import django

from core.models import User


class UserFactory(django.DjangoModelFactory):
	class Meta:
		model=User

	username="test_username"
	password="test_password0"
	first_name="test"
	last_name="test",
	email="test@email.com"
	is_superuser=True