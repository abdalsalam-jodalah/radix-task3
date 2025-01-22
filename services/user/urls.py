from django.urls import path, include
from .views import   *

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),  
    path('login/', UserLoginView.as_view(), name='login'),  
    path('users/', UserListView.as_view(), name='list_users'), 
    path('users/<int:user_id>/', UserDetailView.as_view(), name='get_user'), 
    path('users/edit/<int:user_id>/', UserUpdateView.as_view(), name='edit_user'),  
    path('users/delete/<int:user_id>/', UserDeleteView.as_view(), name='delete_user'),  
]
