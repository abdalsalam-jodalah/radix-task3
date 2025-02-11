from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from ..permissions.user_permissions import IsSingleDevice
from ..models.user_models import User
from ..components.user_components import UserComponents, UserDeviceComponents


class AuthApi(APIView):
    def get_permissions(self):
        """Return the permissions for the current request."""
        if self.request.method == 'POST':
            return [] 
        else:
            return [IsAuthenticated(), IsSingleDevice()] 
        
    def post(self, request):
        request_data = UserComponents.fetch_user_request(request)

        required_fields = ["username", "password", "device_name", "device_type", "user_agent"]
        if not all(request_data.get(field) for field in required_fields):
            return Response({"error": "Missing required fields in request."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserComponents.authenticate_user(username=request_data["username"], password=request_data["password"])
        if not user:
            return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

        data = UserComponents.sign_user(user, request_data["device_name"], request_data["device_type"], request_data["user_agent"])
        if not data or "refresh" not in data or "access_token" not in data:
            return Response({"error": "Error signing user, invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Login successful!',
            'access_token': data["access_token"],
            'refresh_token': str(data["refresh"])
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            request_data = UserComponents.fetch_user_request(request)

            if not all(request_data.get(field) for field in ["device_name", "device_type", "user_agent"]):
                return Response({"error": "Missing required headers."}, status=status.HTTP_400_BAD_REQUEST)

            token = UserComponents.extract_token(request_data["auth_header"])
            if not token:
                return Response({"error": "User token not found."}, status=status.HTTP_400_BAD_REQUEST)

            user_id = UserComponents.extract_user_id_from_auth_header(request_data["auth_header"])
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

            device_identifier = UserDeviceComponents.generate_device_id(user_id, request_data["device_name"], request_data["device_type"], request_data["user_agent"])
            if not device_identifier:
                return Response({"error": "Missing headers for device identification."}, status=status.HTTP_400_BAD_REQUEST)

            UserDeviceComponents.logout_device_basedon_token(device_identifier)
            UserComponents.logout_user(user)
            UserComponents.logout_token(token)
            logout(request)

            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    code = request.GET.get('code')
    error = request.GET.get('error')
    error_description = request.GET.get('error_description')

    if error:
        return Response({"status": "error", "error": error, "description": error_description}, status=400)
    if code:
        return Response({"status": "success", "code": code})
    return Response({"status": "error", "message": "No code provided"}, status=400)

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
