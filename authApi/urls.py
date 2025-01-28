
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
# from oauth2_provider.views import AuthorizationView
from services.user.views import *  
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    # OAuth with local app urls, i just comment it becouse i removed oauth2_provider library during testing google log in 

    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('o/authorize', AuthorizationView.as_view(), name='authorize') ,
    # path('o/authorized/', authorized_view, name='authorized'),
    # path("", include('services.user.urls') ),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', dashboard2, name='dashboard'),
    path('logout/', custom_logout, name='logout'),  # Logout endpoint

]
# http://127.0.0.1:8000/o/authorize/?response_type=code&client_id=4ol8h1JHC5O0yGodqmbjyBAnOkZrYHCbsnkJYIqp&redirect_uri=http://127.0.0.1:8000/o/authorized/&scope=read write&code_challenge=<code_challenge>&code_challenge_method=S256
