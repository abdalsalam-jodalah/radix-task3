from .models import User, UserDevice
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  
from django.utils.timezone import now
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

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
    def authenticate_user(username, password,):
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
    
    def register_device(user, device_name, device_type, device_token):
        # Ensure the device is unique or update if it exists
        device, created = UserDevice.objects.update_or_create(
            user=user,
            device_token=device_token or 12,
            defaults={
                "device_name": device_name or "Unknown Device",
                "device_type": device_type or "Unknown Type",
                "is_active": True,
                "login_time": now(),
                "logout_time": None
            }
        )
        if not created:
            device.is_active = True
            device.login_time = now()
            device.logout_time = None
            device.save()

    
    def logout_device(user, device_token):
        try:
            device = UserDevice.objects.get(user=user, device_token=device_token, is_active=True)
            device.is_active = False
            device.logout_time = now()
            device.save()
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
         
    def logout_all_devices(user):
        user.is_logedin = False
        user.save()
        # UserDevice.objects.filter(user=user, is_active=True).update(is_active=False, logout_time=now())

        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            try:
                token.blacklist()
            except Exception as e:
                raise Exception(f"Error blacklisting token: {e}")