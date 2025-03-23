from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from ..models.user_models import User
from ..models.user_device_models import UserDevice
from .user_components import UserComponents
from .user_device_components import UserDeviceComponents
import json
import jwt
from django.conf import settings

class AuthComponents():
    @staticmethod
    def fetch_user_data(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            body_data = {}

        email = body_data.get("email")
        password = body_data.get("password")
        if not email:
            raise ValidationError({"error": "Email is required."})
        if not password:
            raise ValidationError({"error": "Password is required."})
        return {"email": email, "password": password}
  
    @staticmethod
    def fetch_auth_header(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise ValidationError({"error": "auth_header is required."})
        return auth_header


    @staticmethod
    def fetch_user_request(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        device_name = request.headers.get("Device-Name", "Unknown Device")
        device_type = request.headers.get("Device-Type", "Unknown Device")
        user_agent = request.headers.get("User-Agent", "Unknown User Agent")

        if not device_name:
            raise ValidationError({"error": "device_name is required."})
        if not device_type:
            raise ValidationError({"error": "device_type is required."})
        if not user_agent:
            raise ValidationError({"error": "user_agent is required."})
        
        return {
            "device_name": device_name,
            "device_type": device_type,
            "user_agent": user_agent,
        }

    @staticmethod
    def authenticate_user(email, password):
        user = UserComponents.get_user_by_email(email)
        if not user:
            raise User.DoesNotExist({"error": "User not found. sign up"})
        
        if not user.password.startswith('pbkdf2_'):
            user.password = make_password(user.id) 
            user.save()

        if not user.check_password(password):
            raise AuthenticationFailed({"error": "Incorrect password. try again"})
        
        return user

    @staticmethod
    def sign_user(user, device_name, device_type , user_agent ):
        device_token = UserDeviceComponents.generate_device_id(user.id, device_name, device_type, user_agent)
        device = UserDeviceComponents.fetch_device_by_user_and_token(user, device_token)

        status = UserDeviceComponents.authenticate_device(user, device)
        # if status.get("status") == "exist_active":
        #     raise ValidationError("This device is already registered and active.")
        UserDeviceComponents.logout_all_devices_for_user(user)

        UserDeviceComponents.register_device(user, device, device_token, status)
     
        refresh_token = AuthComponents.create_token(user)
        UserComponents.set_login_status(user, True) 
        if not refresh_token:
            return None
        
        return {
            "refresh_token": str(refresh_token), 
            "access_token":str(refresh_token.access_token)
                }
    
    @staticmethod
    def create_token(user):
        refresh = RefreshToken.for_user(user)
        if not refresh:
           return Response({"error": "refresh token has problem "}, status=status.HTTP_226_IM_USED)
        return refresh

    def get_user(request):
        try:
            auth_header= AuthComponents.fetch_auth_header(request)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

        user_id = AuthComponents.extract_user_id_from_auth_header(auth_header)
        if not user_id:
            return Response({"error": "Token not valid."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        return user 
    
    def extract_user_id_from_auth_header(auth_header):
        try:
            token_str = AuthComponents.extract_token(auth_header)
            return token_str.payload["user_id"]  
        except Exception as err:
            return None  

    def extract_user_id_from_request(request):
        auth_header= request.headers.get("Authorization")
        return AuthComponents.extract_user_id_from_auth_header(auth_header)
    


    
    def logout_token(token):
        # i think no need to distroy token since i made new  permission : IsSingleDevice, but i kept it ensure that 
        pass
    
    def logout_user(user):
        try:
            user.is_logged_in = False
            user.save()
        except UserDevice.DoesNotExist:
            raise ValidationError("User not found or already logged out.")
    def extract_token(auth_header):
        if not auth_header:
            return None

        if auth_header.startswith("Bearer "):
            parts = auth_header.split(" ")
            if len(parts) == 2:
                token_str = parts[1]
            else:
                token_str = parts[2]

        else:
            token_str = auth_header

        try:
            token = AccessToken(token_str)
            return token
        except Exception as err:
            print(err)
            return None


    def decode_expired_token(auth_header):
        if not auth_header:
            return None

        if auth_header.startswith("Bearer "):
            parts = auth_header.split(" ")
            if len(parts) == 2:
                token_str = parts[1]
            else:
                token_str = parts[2]
        else:
            token_str = auth_header

        try:
            decoded = jwt.decode(token_str, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
            return decoded
        except jwt.InvalidTokenError as err:
            print(err)
            return None

         




