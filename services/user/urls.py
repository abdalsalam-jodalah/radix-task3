from django.urls import path, include
from .views import   *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from oauth2_provider.views import TokenView, RevokeTokenView
# from oauth2_provider.views import TokenView, AuthorizationView
# from oauth2_provider.views import AuthorizationView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),  
    path('login/', UserLoginView.as_view(), name='login'),  
    path('logout/', UserLogoutView.as_view(), name='logout'),  
    path('logout/all', UserLogoutAllView.as_view(), name='logout_all_devices'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserListView.as_view(), name='list_users'), 
    path('users/<int:id>/', UserDetailView.as_view(), name='get_user'), 
    path('users/edit/<int:id>/', UserUpdateView.as_view(), name='edit_user'),  
    path('users/delete/<int:id>/', UserDeleteView.as_view(), name='delete_user'), 

    path('accounts/', include('allauth.urls')),
    path('dashboard/', dashboard2, name='dashboard'),
    path('logout/', custom_logout, name='logout'),  # Logout endpoint

    # OAuth with local app urls, i just comment it becouse i removed oauth2_provider library during testing google log in 
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('o/authorize', AuthorizationView.as_view(), name='authorize') ,
    # path('o/authorized/', authorized_view, name='authorized'), 
]
# http://127.0.0.1:8000/o/authorize/?response_type=code&client_id=4ol8h1JHC5O0yGodqmbjyBAnOkZrYHCbsnkJYIqp&redirect_uri=http://127.0.0.1:8000/o/authorized/&scope=read write&code_challenge=<code_challenge>&code_challenge_method=S256
