from django.urls import path

from bot.views import VerifyView

urlpatterns = [
    path("verify", VerifyView.as_view()),
]
