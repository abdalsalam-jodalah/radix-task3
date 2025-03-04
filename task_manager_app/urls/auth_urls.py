from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from ..controllers.auth_controllers import   AuthApi
# from ..controllers.auth_controllers import    dashboard, custom_logout

# from oauth2_provider.views import TokenView, RevokeTokenView
# from oauth2_provider.views import TokenView, AuthorizationView
# from oauth2_provider.views import AuthorizationView

urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/',           AuthApi.as_view(), name='login'),  
    path('auth/logout/',           AuthApi.as_view(), name='logout'),  
    # path('accounts/', include('allauth.urls')),
    # path('dashboard/', dashboard, name='dashboard'),
    # path('oauth/logout/', custom_logout, name='logout'),  # Logout endpoint

    # OAuth with local app urls, i just comment it becouse i removed oauth2_provider library during testing google log in 
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('o/authorize', AuthorizationView.as_view(), name='authorize') ,
    # path('o/authorized/', authorized_view, name='authorized'), 
]
# http://127.0.0.1:8000/o/authorize/?response_type=code&client_id=4ol8h1JHC5O0yGodqmbjyBAnOkZrYHCbsnkJYIqp&redirect_uri=http://127.0.0.1:8000/o/authorized/&scope=read write&code_challenge=<code_challenge>&code_challenge_method=S256
