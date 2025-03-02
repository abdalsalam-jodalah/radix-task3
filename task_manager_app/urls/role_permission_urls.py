from django.urls import path
from ..controllers.user_controllers import   UserApi
from ..controllers.role_permission_controllers import RoleApi, PermissionApi
urlpatterns = [
    path('role/',          RoleApi.as_view(), name='role_crud'  ), 
    path('role/<int:id>/', RoleApi.as_view(), name='role_id_crud'), 
    path('permission/',          PermissionApi.as_view(), name='permission_crud'  ), 
    path('permission/<int:id>/', PermissionApi.as_view(), name='permission_id_crud'), 
]