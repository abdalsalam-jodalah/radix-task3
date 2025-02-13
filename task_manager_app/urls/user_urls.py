from django.urls import path

from ..controllers.user_controllers import   UserApi

urlpatterns = [
    path('user/',          UserApi.as_view(), name='users_crud'  ), 
    path('user/<int:id>/', UserApi.as_view(), name='user_id_crud'), 
]