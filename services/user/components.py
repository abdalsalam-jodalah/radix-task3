from .models import User, UserDevice
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from django.utils.timezone import now
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

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
    
    # def register_device(user, device_name, device_type, device_token):
    #     # Ensure the device is unique or update if it exists
    #     device, created = UserDevice.objects.update_or_create(
    #         user=user,
    #         device_token=device_token ,
    #         defaults={
    #             "device_name": device_name or "Unknown Device",
    #             "device_type": device_type or "Unknown Type",
    #             "is_active": True,
    #             "login_time": now(),
    #             "logout_time": None
    #         }
    #     )
    #     if not created:
    #         device.is_active = True
    #         device.login_time = now()
    #         device.logout_time = None
    #         device.save()

    def register_device(user, device_name, device_type, device_token):
        # Ensure a device is unique per user
        existing_device = UserDevice.objects.filter(user=user, device_token=device_token).first()

        if existing_device:
            # Update existing device status if found
            existing_device.is_active = True
            existing_device.login_time = now()
            existing_device.logout_time = None
            existing_device.save()
        else:
            # Create new device entry if it doesn't exist
            UserDevice.objects.create(
                user=user,
                device_name=device_name or "Unknown Device",
                device_type=device_type or "Unknown Type",
                device_token=device_token,
                is_active=True,
                login_time=now(),
                logout_time=None
            )


    def logout_user(user):
        try:
            user.is_logedin = False
            user.save()
        except UserDevice.DoesNotExist:
            raise ValidationError("User not found or already logged out.")
         
    def logout_device(device_identifier):
        try:
            device = UserDevice.objects.get( device_token =  device_identifier.lower())
            device.is_active = False
            device.logout_time = now()
            device.save()
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
         
    def logout_all_devices(user):
        user.is_logedin = False
        user.save()
        # UserDevice.objects.filter(user=user, is_active=True).update(is_active=False, logout_time=now())
        devices = UserDevice.objects.filter( user_id =  user.user_id)
        for device in devices:
        # Set device status as inactive and log out time
            device.is_active = False
            device.logout_time = now()
            device.save()  # Save the device object to persist changes

        try:
            tokens = OutstandingToken.objects.get()
            for token in tokens:
                
            # Add token to BlacklistedToken table
                BlacklistedToken.objects.create(token=token)
        except Exception as e:
             raise ValidationError(f"Error blacklisting tokens: {e}")
    # def extract_user_id_from_token(request):
    #     auth_header = request.headers.get("Authorization")

    #     if not auth_header or not auth_header.startswith("Bearer "):
    #         return JsonResponse({"error": "Invalid or missing token"}, status=400)

    #     try:
    #         # Extract only the token part
    #         token_str = auth_header.split(" ")[1]

    #         # Decode the token
    #         token = AccessToken(token_str)
    #         user_id = token["user_id"]  # Extract user ID from token payload

    #         return JsonResponse({"user_id": user_id})

    #     except Exception as e:
    #         return JsonResponse({"error": "Invalid or expired token"}, status=400)

    def extract_user_id_from_token(request):
        auth_header = request.headers.get("Authorization")
       
        if not auth_header or not auth_header.startswith("Bearer "):
            
            return None  # Return None if the token is missing or invalid
       
        try:
          
            token_str = auth_header.split(" ")[2]  # Extract the token part
           
            token = AccessToken(token_str)  # Decode the token
            

            return token["user_id"]  # Return the user ID directly

        except Exception:
            return None  # Return None if the token is invalid or expired
