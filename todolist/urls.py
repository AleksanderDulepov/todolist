from django.contrib import admin
from django.urls import path, include

from core.urls import router_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router_user.urls)),
]
