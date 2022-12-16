from django.urls import path

from core.views import UserCreateView, UserLoginView, UserProfileView

urlpatterns=[path('signup', UserCreateView.as_view()),
			 path('login', UserLoginView),
			 path('profile', UserProfileView.as_view()),
		    ]