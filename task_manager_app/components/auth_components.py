from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from ..repositories.user_repository import UserRepository
from ..models.user_models import User
from ..models.user_device_models import UserDevice
from .user_components import UserComponents
from .user_device_components import UserDeviceComponents
import json
import jwt
from django.conf import settings
from rest_framework_simplejwt.exceptions  import TokenError

class AuthComponents():
    @staticmethod
    def fetch_login_data_from_req(request):
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
    def fetch_signup_data_from_req(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            body_data = {}

        email = body_data.get("email")
        password = body_data.get("password")
        first_name = body_data.get("first_name")
        last_name = body_data.get("last_name")
        if not email:
            raise ValidationError({"error": "Email is required."})
        if not password:
            raise ValidationError({"error": "Password is required."})
        if not first_name:
            raise ValidationError({"error": "first_name is required."})
        if not last_name:
            raise ValidationError({"error": "last_name is required."})
                
        return {"email": email, 
                "password": password,
                "first_name": first_name,
                "last_name": last_name}
  
    @staticmethod
    def fetch_auth_header_from_req(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise ValidationError({"error": "auth_header is required."})
        return auth_header


    @staticmethod
    def fetch_headers_from_req(request):
        if request is None:
            raise ValidationError({"error": "Request object is required."})
        device_name = request.headers.get("Device-Name")
        device_type = request.headers.get("Device-Type")
        user_agent = request.headers.get("User-Agent")

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
        UserDeviceComponents.logout_all_devices_for_user(user)
        UserDeviceComponents.register_device(user, device, device_token, status)
        refresh_token = AuthComponents.create_token(user)
        if not refresh_token:
            raise ValidationError({"error": "making token failed"})
        
        UserComponents.set_login_status(user, True) 

        return {
            "refresh_token": str(refresh_token), 
            "access_token":str(refresh_token.access_token)
                }
    
    @staticmethod
    def create_token(user):
        refresh = RefreshToken.for_user(user)
        if not refresh:
           raise ValidationError({"error": "refresh token has problem "})
        return refresh
    
    @staticmethod
    def fetch_token_from_req(request):
        if not request:
            raise ValidationError({"error": "Request object is required."})
        try:
            auth_header = AuthComponents.fetch_auth_header_from_req(request)
        
            if not auth_header:
                raise ValidationError({"error": "Authorization header is required."})
            
            token_str = None

            if auth_header.startswith("Bearer "):
                parts = auth_header.split(" ")
                if len(parts) >= 2:
                    token_str = parts[2]
                else:
                    token_str = parts[1]
            else:
                token_str = auth_header
            
            if not token_str or token_str == "Bearer":
                raise ValidationError({"error": "Token not found in header."})
            token = AccessToken(token_str)
            if not token:
                raise ValidationError({"error": "Invalid access token."})
            return token
        except TokenError as e:
            raise TokenError({"error": f"Error fetching token. {e}", "token": token_str})
        except Exception as e:
            raise ValidationError({"error": f"Error fetching token. {e}"})


    @staticmethod
    def extract_userid_from_token(token):
        user_id = token.payload["user_id"]
        if not user_id:
            raise ValidationError({"error": "Invalid token. user id not found in token."})
        return token.payload["user_id"]
    
    @staticmethod
    def fetch_user_based_on_token(token):
        user_id= AuthComponents.extract_userid_from_token(token)
        if not user_id:
            raise ValidationError({"error": "Invalid token. user id not found in token."})
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        return user 
    
    @staticmethod
    def fetch_user_from_req(request):
        token = AuthComponents.fetch_token_from_req(request)
        if not token: 
            raise ValidationError({"error": "Token not valid"})
        user = AuthComponents.fetch_user_based_on_token(token)
        if not user or not isinstance(user, User): 
            raise ValidationError({"error": "while fetching user,Token not valid or user not found."})
        return user
    
    @staticmethod
    def logout_user(user):
        if not user or not isinstance(user, User):
            raise ValidationError({"error": "User is required."})
        UserRepository.set_user_attribute(user, 'is_logged_in', False)
  
    @staticmethod
    def logout_token(token):
        # TODO: implement this method, maybe block the token
            #old:    # i think no need to distroy token since i made new  permission : IsSingleDevice, but i kept it ensure that 
        pass
    




    def get_user(request):
        try:
            auth_header= AuthComponents.fetch_auth_header_from_req(request)
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
            return None


    def decode_expired_token(token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
            return decoded
        except jwt.InvalidTokenError as err:
            return None

