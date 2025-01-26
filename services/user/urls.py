from django.urls import path, include
from .views import   *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),  
    path('login/', UserLoginView.as_view(), name='login'),  
    path('users/', UserListView.as_view(), name='list_users'), 
    path('users/<int:id>/', UserDetailView.as_view(), name='get_user'), 
    path('users/edit/<int:id>/', UserUpdateView.as_view(), name='edit_user'),  
    path('users/delete/<int:id>/', UserDeleteView.as_view(), name='delete_user'), 
     
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
