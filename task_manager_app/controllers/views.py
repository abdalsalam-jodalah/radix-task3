from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..models.user_models import User
from ..components.user_components import UserComponents, UserDeviceComponents
from authApi.pagination import CustomPagination

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,IsSingleDevice]
    pagination_class = CustomPagination # /api/tasks/?page=2&page_size=5

    def get_queryset(self):
        return UserComponents.get_all_users()
    
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, IsSingleDevice]
    def get_queryset(self):
        user_id = self.kwargs.get('id')  
        return UserComponents.get_user_by_id(user_id)    

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
   
    def perform_create(self, serializer):
        UserComponents.create_user(serializer.validated_data) 

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, IsSingleDevice]

    def perform_update(self, serializer):
        UserComponents.update_user(serializer.validated_data) 

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, IsSingleDevice]

class UserLoginView(APIView):
    def post(self, request):
        request_data =UserComponents.fetch_user_request(request)
        if not request_data["username"] or not request_data["password"]:
            return Response({"error": "user's credentials should be exist in request."}, status=status.HTTP_400_BAD_REQUEST)
        if not ["device_name"] or not request_data["device_type"] or not request_data["user_agent"]:
            return Response({"error": "request's headers must be attached."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserComponents.authenticate_user(username=request_data["username"], password=request_data["password"])
        if user:
            data= UserComponents.sign_user(user,request_data["device_name"], request_data["device_type"], request_data["user_agent"])
            if not data or "refresh" not in data or "access_token" not in data:
                return Response({"error": "User signing has an error, and token is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Login successful!',
                'access_token': data["access_token"],
                'refresh_token': str(data["refresh"])
            })   
        return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated, IsSingleDevice]

    def post(self, request):
        try:
            request_data =UserComponents.fetch_user_request(request)
            if not request_data["device_name"] or not request_data["device_type"] or not request_data["user_agent"]:
               return Response({"error": "request's headers must be attached."}, status=status.HTTP_400_BAD_REQUEST)

            user_id = UserComponents.extract_user_id_from_auth_header(request_data["auth_header"])
            if not user_id:
                return Response({"error":"user token notfound."})
            
            token = UserComponents.extract_token(request_data["auth_header"])
            if not token:
                return Response({"error":"user token not found."})
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValidationError("User not found!")

            device_identifier = UserDeviceComponents.generate_device_id(user_id, request_data["device_name"], request_data["device_type"], request_data["user_agent"])
            if device_identifier is  None:
                return Response({"error":"there are missing headers attrs"})
    
            UserDeviceComponents.logout_device_basedon_token(device_identifier)
            UserComponents.logout_user(user)
            UserComponents.logout_token(token)
            logout(request) 
            
            return Response({"message": "Logout successful!"}, status=200)
            return redirect("https://127.0.0.1/login")

        except Exception as e:
            return Response({"error": str(e)}, status=400)
   
class UserLogoutAllView(APIView):
    permission_classes = [IsAuthenticated, IsSingleDevice]

    def post(self, request):
        try:
            request_data =UserComponents.fetch_user_request(request)
            token = UserComponents.extract_token(request_data["auth_header"])
            if not token:
                return Response({"error":"user token not found."})
            
            user_id = UserComponents.extract_user_id_from_auth_header(request_data["auth_header"])
            if not user_id:
                return Response({"error":"user not found - token invalid."})
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise ValidationError("User not found!")

            UserDeviceComponents.logout_all_devices_for_user(user)  
            UserComponents.logout_user(user)
            UserComponents.logout_token(token)
            logout(request) 

            return Response({"message": "Logged out from all devices successfully!"}, status=status.HTTP_200_OK)
            return redirect("https://127.0.0.1/login")

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def authorized_view(request):
    code = request.GET.get('code', None)
    error = request.GET.get('error', None)
    error_description = request.GET.get('error_description', None)

    if error:
        return Response({
            'status': 'error',
            'error': error,
            'description': error_description
        }, status=400)
    if code:
        return Response({'status': 'success', 'code': code})
    return Response({'status': 'error', 'message': 'No code provided'}, status=400)

@login_required
def dashboard(request):
    
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
