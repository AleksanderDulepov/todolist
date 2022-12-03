from django.db import router
from django.urls import path
from rest_framework.routers import SimpleRouter

from core.views import UserViewSet

router_user=SimpleRouter()
router_user.register('user', UserViewSet)