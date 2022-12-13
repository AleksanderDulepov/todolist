from django.urls import path

from core.views import UserCreateView

urlpatterns=[path('signup/', UserCreateView.as_view()),
	     # path('login/', UserLoginView)
		    ]