from django.urls import path, include
from .views import   *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from oauth2_provider.views import TokenView, RevokeTokenView
from oauth2_provider.views import TokenView, AuthorizationView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),  
    path('login/', UserLoginView.as_view(), name='login'),  
    path('users/', UserListView.as_view(), name='list_users'), 
    path('users/<int:id>/', UserDetailView.as_view(), name='get_user'), 
    path('users/edit/<int:id>/', UserUpdateView.as_view(), name='edit_user'),  
    path('users/delete/<int:id>/', UserDeleteView.as_view(), name='delete_user'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('o/token/', TokenView.as_view(), name='token'),
    # path('o/revoke_token/', RevokeTokenView.as_view(), name='revoke_token'),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('auth/', include('dj_rest_auth.urls')),  
    path('auth/social/', include('allauth.socialaccount.urls')), 

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('o/authorize/', AuthorizationView.as_view(), name='authorize'),
    path('o/token/', TokenView.as_view(), name='token'),
]
