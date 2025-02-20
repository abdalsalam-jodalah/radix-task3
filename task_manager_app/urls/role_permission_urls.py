from django.urls import path
from ..controllers.user_controllers import   UserApi

urlpatterns = [
    path('role/',          UserApi.as_view(), name='role_crud'  ), 
    path('role/<int:id>/', UserApi.as_view(), name='role_id_crud'), 
    path('permission/',          UserApi.as_view(), name='permission_crud'  ), 
    path('permission/<int:id>/', UserApi.as_view(), name='permission_id_crud'), 
]