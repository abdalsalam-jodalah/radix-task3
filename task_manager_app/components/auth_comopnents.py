from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from ..models.user_models import User
from ..models.user_device_mdoels import UserDevice
from .user_components import UserComponents
from .user_device_components import UserDeviceComponents
import json

class AuthComponents():
    def authenticate_user(email, password):
        try:
            user = UserComponents.get_user_by_email(email)
            if not user.password.startswith('pbkdf2_'):
                user.password = make_password(user.id) 
                user.save()
        except User.DoesNotExist:
            return None
        except Exception as err:
            return None
        if not user.check_password(password):
            return None
        return user
    
    def logout_token(token):
        # i think no need to distroy token since i made new  permission : IsSingleDevice, but i kept it ensure that 
        pass
    
    def logout_user(user):
        try:
            user.is_logedin = False
            user.save()
        except UserDevice.DoesNotExist:
            raise ValidationError("User not found or already logged out.")
    def extract_token(auth_header):
        if not auth_header or not auth_header.startswith("Bearer "):
            return None 
        try:
            token_str = auth_header.split(" ")[2]  
            token = AccessToken(token_str) 
            return token
        except Exception:
            return None  
    def extract_user_id_from_request(request):
        auth_header= request.headers.get("Authorization")
        return AuthComponents.extract_user_id_from_auth_header(auth_header)
    
    def extract_user_id_from_auth_header(auth_header):
        try:
            token_str = AuthComponents.extract_token(auth_header)
            return token_str.payload["user_id"]  
        except Exception as err:
            return None  
        
    def fetch_user_data(request):
        try:
            body_data = json.loads(request.body.decode('utf-8')) 
        except json.JSONDecodeError:
            body_data = {}  
        
        return {
            "email": body_data.get("email"),
            "password": body_data.get("password")
        }

    
    def fetch_user_request(request):
       return {
            "device_name": request.headers.get( "device_name", "Unknown Device"),
            "device_type": request.headers.get( "device_type", "Unknown Device"),
            # "device_name": request.headers.get("Sec-Ch-Ua-Platform" | "device_name", "Unknown Device"),
            # "device_type": request.headers.get("Sec-Ch-Ua"| "device_type", "Unknown Device"),
            "user_agent": request.headers.get("User-Agent", "Unknown User Agent"),
            "auth_header": request.headers.get("Authorization")
        }

    def sign_user(user, device_name, device_type , user_agent ):
        if isinstance(user, User):
            device_identifier = UserDeviceComponents.generate_device_id(user.id, device_name, device_type, user_agent)

        device = UserDeviceComponents.authenticate_device(user, device_identifier)
        if device.get("status") == "exist_active":
            return Response({"error": "This device is already registered and active."}, status=status.HTTP_226_IM_USED)
        refresh = RefreshToken.for_user(user)

        if not refresh:
           return Response({"error": "refresh token has problem "}, status=status.HTTP_226_IM_USED)
        try:
            UserDeviceComponents.logout_all_devices_for_user(user)

        except UserDevice.DoesNotExist:
            pass

        UserDeviceComponents.register_device(user, device_name, device_type, device_identifier, device.get("status"))
     
        if isinstance(user, User): 
            user.is_logedin = True
            user.save()

        else:
            return Response({"error": "User not found or invalid."}, status=status.HTTP_404_NOT_FOUND)
    
        return {
            "refresh": refresh, 
            "access_token":str(refresh.access_token)
                }
    
    def get_user(request):
        request_data= AuthComponents.fetch_user_request(request)
        if not request_data["auth_header"]: 
            return Response({"error": "Missing required headers."}, status=status.HTTP_400_BAD_REQUEST)
        user_id = AuthComponents.extract_user_id_from_auth_header(request_data["auth_header"])
        if not user_id:
            return Response({"error": "Token not valid."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        return user 
