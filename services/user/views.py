from rest_framework import status, generics
from .serializers import UserSerializer
from .models import User
from .components import UserComponents
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
import uuid
class UserListView(generics.ListAPIView):

    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return UserComponents.get_all_users()
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    lookup_field = 'id'           # back here
    permission_classes=[IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        UserComponents.create_user(serializer.validated_data) 

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    def perform_update(self, serializer):
        UserComponents.update_user(serializer.validated_data) 

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        device_name = request.headers.get('Sec-Ch-Ua-Platform', 'Unknown Device')
        device_type = request.headers.get('Sec-Ch-Ua', 'Unknown Device')
        user_agent = request.headers.get('User-Agent', 'Unknown User Agent')
        csrf_token = request.headers.get('X-Csrftoken')
        cookies = request.headers.get('Cookie')
        content_type = request.headers.get('Content-Type')
        
        device_token = str(uuid.uuid4())    
        print("request:", request.headers)
        user = UserComponents.authenticate_user(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            UserComponents.register_device(user, device_name, device_type, device_token)

            user.is_logedin =True
            user.save()
            return Response({
                'message': 'Login successful!',
                'access_token': access_token,
                'refresh_token': str(refresh)
            })   
        return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            device_token = request.data.get('device_token')
            if device_token:
                UserComponents.logout_device(user, device_token)

            user.is_logedin = False
            user.save()

            refresh_token = request.data.get("refresh_token")  
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  
            logout(request) 
            
            return Response({"message": "Logout successful!"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
   
class UserLogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            UserComponents.logout_all_devices(user)  
            return Response({"message": "Logged out from all devices successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def authorized_view(request):
    code = request.GET.get('code', None)
    error = request.GET.get('error', None)
    error_description = request.GET.get('error_description', None)

    if error:
        return JsonResponse({
            'status': 'error',
            'error': error,
            'description': error_description
        }, status=400)
    if code:
        return JsonResponse({'status': 'success', 'code': code})
    return JsonResponse({'status': 'error', 'message': 'No code provided'}, status=400)


@login_required
def dashboard2(request):
    
    user = request.user
    social_account = user.socialaccount_set.filter(provider='google').first()
    google_data = social_account.extra_data if social_account else {}
    user.is_logedin = True
    user.save()
    return render(request, 'dashboard.html', {'user': user, 'google_data': google_data})

@login_required
def custom_logout(request):
    user = request.user
    user.is_logedin = False
    user.save()

    logout(request)

    return redirect('account_login')
