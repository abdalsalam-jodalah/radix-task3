import hashlib
from .models import User, UserDevice
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class UserComponents():
    def get_all_users():
        return User.objects.all()

    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found!")

    def create_user(user_data):
        user = User(**user_data)
        user.save()

    def update_user(user_data):
        user = User.objects.get(id=user_data['id'])
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()

    def authenticate_user(username, password):
        try:
            user = User.objects.get(username=username)
            if not user.password.startswith('pbkdf2_'):
                user.password = make_password(user.password) 
                user.save()
        except User.DoesNotExist:
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

    def extract_user_id_from_auth_header(auth_header):
        try:
            token_str = UserComponents.extract_token(auth_header)
            return token_str.payload["user_id"]  
        except Exception as err:
            return None  
        
    def fetch_user_request(request):
       return {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
            "device_name": request.headers.get("Sec-Ch-Ua-Platform", "Unknown Device"),
            "device_type": request.headers.get("Sec-Ch-Ua", "Unknown Device"),
            "user_agent": request.headers.get("User-Agent", "Unknown User Agent"),
            "auth_header":request.headers.get("Authorization")
        }
    #########################################################################################
    def sign_user(user, device_name, device_type , user_agent ):# i feel it should not be extracted from UserLoginView
        device_identifier = UserDeviceComponents.generate_device_id(user.id, device_name, device_type, user_agent)
        device = UserDeviceComponents.authenticate_device(user, device_identifier)
        if device.get("status") == "exist_active":
            return Response({"error": "This device is already registered and active."}, status=status.HTTP_226_IM_USED)

        refresh = RefreshToken.for_user(user)
        UserDeviceComponents.logout_all_devices_for_user(user)
        UserDeviceComponents.register_device(user, device_name, device_type, device_identifier, device.get("status"))
        user.is_logedin =True
        user.save()
        return refresh
    
class UserDeviceComponents():
    def generate_device_id(user_id, device_name, device_type,user_agent):
        raw_data = f"{user_id}-{device_name}-{device_type}-{user_agent}"
        return hashlib.sha256(raw_data.encode()).hexdigest()

    def authenticate_device(user, device_token ):
        existing_device = UserDevice.objects.filter(user=user, device_token=device_token).first()

        if existing_device and existing_device.is_active:
            return {"status": "exist_active"}
        if existing_device and not existing_device.is_active:
            return {"status": "exist_not_active"}
        return {"status": "not_exist"}
        
    def register_device(user, device_name, device_type, device_token,status):
        if status == "exist_not_active" :
            existing_device = UserDevice.objects.filter(user=user, device_token=device_token).first()
            existing_device.is_active = True
            existing_device.login_time = now()
            existing_device.logout_time = None
            existing_device.save()
        elif status == "not_exist" :
            UserDevice.objects.create(
                user=user,
                device_name=device_name or "Unknown Device",
                device_type=device_type or "Unknown Type",
                device_token=device_token,
                is_active=True,
                login_time=now(),
                logout_time=None
            )
    def logout_device_basedon_token(device_identifier):
        try:
            device = UserDevice.objects.get(device_token=device_identifier.lower())
            UserDeviceComponents.logout_device(device)
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
         
    def logout_all_devices_for_user(user):
        try:
            devices = UserDevice.objects.filter(user_id=user.id)
            for device in devices:
                UserDeviceComponents.logout_device(device)
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
    
    def logout_device(device):
        device.is_active = False
        device.logout_time = now()
        device.save()  