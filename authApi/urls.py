
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager api",
        default_version='v1',
        description="API for managing tasks and users with JWT authentication.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="License"),
        authentication_classes=[],  
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('task_manager_app.urls.user_urls') ),
    path("", include('task_manager_app.urls.task_urls') ),
    path("", include('task_manager_app.urls.auth_urls') ),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
