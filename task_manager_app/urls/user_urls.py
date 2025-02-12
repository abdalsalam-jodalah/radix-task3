from django.urls import path

from ..controllers.user_controllers import   UserApi

urlpatterns = [
    path('users/',          UserApi.as_view(), name='users_crud'  ), 
    path('users/<int:id>/', UserApi.as_view(), name='user_id_crud'), 
]