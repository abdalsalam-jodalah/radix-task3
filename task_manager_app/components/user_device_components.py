import hashlib
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from ..repositories.user_device_repository import UserDeviceRepository
from ..models.user_device_mdoels import UserDevice


class UserDeviceComponents():
    def generate_device_id(user_id, device_name, device_type,user_agent):
        raw_data = f"{user_id}-{device_name}-{device_type}-{user_agent}"
        return raw_data
        # return hashlib.sha256(raw_data.encode()).hexdigest()

    def authenticate_device(user, device_token):
        try:
            existing_device = UserDeviceRepository.fetch_Device_by_userid_token(user, device_token)

            if existing_device:
                device = existing_device 
                if device.is_active:
                    return {"status": "exist_active"}
                else:
                    return {"status": "exist_not_active"}
            else:
                return {"status": "not_exist"}
        
        except Exception as err:
            print(f"exception {err}")


    def register_device(user, device_name, device_type, device_token,status):
        if status == "exist_not_active" :
            existing_device = UserDeviceRepository.fetch_Device_by_userid_token(user, device_token)
            UserDeviceRepository.activate_device(existing_device, now(), True, None)
        elif status == "not_exist" :
            UserDeviceRepository.create_device(user,device_name,device_type,device_token,True,now(),None)
            
    def logout_device_basedon_token(device_identifier):
        try:
            device = UserDeviceRepository.fetch_Device_by_token(device_token=device_identifier.lower())
            UserDeviceComponents.logout_device(device)
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
         
    def logout_all_devices_for_user(user):
        try:
            devices = UserDeviceRepository.fetch_Device_by_token(user.id)
            for device in devices:
                UserDeviceComponents.logout_device(device)
        except UserDevice.DoesNotExist:
            raise ValidationError("Device not found or already logged out.")
    
    def logout_device(device):
        device.is_active = False
        device.logout_time = now()
        if isinstance(device, UserDevice):
            device.save()  
        else:
            raise ValidationError("Device not found or already logged out.")