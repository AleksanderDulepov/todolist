from django.urls import path

from core.views import UserCreateView, UserLoginView, UserProfileView, UserUpdatePasswordView

urlpatterns = [path('signup', UserCreateView.as_view()),
               path('login', UserLoginView.as_view()),
               path('profile', UserProfileView.as_view()),
               path('update_password', UserUpdatePasswordView.as_view()),
               ]
