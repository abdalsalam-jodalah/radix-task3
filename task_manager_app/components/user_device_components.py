import hashlib
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from ..models.user_device_mdoels import UserDevice


class UserDeviceComponents():
    def generate_device_id(user_id, device_name, device_type,user_agent):
        raw_data = f"{user_id}-{device_name}-{device_type}-{user_agent}"
        return raw_data
        # return hashlib.sha256(raw_data.encode()).hexdigest()

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