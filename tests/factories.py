import factory
from factory import PostGenerationMethodCall

from core.models import User
from goals.models import GoalCategory, Goal, GoalComment


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model=User

	username="test_username"
	first_name="test_first_name"
	last_name="test_last_name"
	email="test@email.com"
	is_superuser=True

	password = PostGenerationMethodCall('set_password',
												'test_password0')


class GoalCategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = GoalCategory

	user = factory.SubFactory(UserFactory)
	created = factory.Faker("date_time")
	updated = factory.Faker("date_time")
	title = "goal_category_title"


class GoalFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Goal

	user = factory.SubFactory(UserFactory)
	created = factory.Faker("date_time")
	updated = factory.Faker("date_time")
	title = "goal_title"
	category = factory.SubFactory(GoalCategoryFactory)
	description = "goal_description"
	status = 1
	priority = 1
	due_date = factory.Faker("date_time")


class GoalCommentFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = GoalComment

	user = factory.SubFactory(UserFactory)
	created = factory.Faker("date_time")
	updated = factory.Faker("date_time")
	goal = factory.SubFactory(GoalFactory)
	text = "goal_comment_text"