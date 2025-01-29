
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('services.user.urls') ),
    path("", include('services.task.urls') ),
]
