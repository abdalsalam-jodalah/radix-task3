from ..models.user_device_mdoels import UserDevice

class UserDeviceRepository():
    def fetch_all_user_devices(user = None):
        if user:
            return UserDevice.objects.filter(user_id=user.id).first()
        return UserDevice.objects.all()
    
    def fetch_Device_by_userid_token(user = None, device_token=None):
        return UserDevice.objects.filter(user_id=user.id, device_token=device_token)
    
    def fetch_Device_by_token( device_token=None):
        return UserDevice.objects.filter( device_token=device_token)
    
    def fetch_Device_by_userid(user_id):
        return UserDevice.objects.filter(user_id=user_id)
    
    def create_device(user,device_name,device_type,device_token,is_active,login_time,logout_time):
        UserDevice.objects.create(
            user=user,
            device_name=device_name or "Unknown Device",
            device_type=device_type or "Unknown Type",
            device_token=device_token,
            is_active=is_active,
            login_time=login_time,
            logout_time=logout_time
        )

    def activate_device(existing_device, login_time, is_active=True,logout_time=None  ):
        existing_device.is_active = is_active
        existing_device.login_time = login_time
        existing_device.logout_time = logout_time
        existing_device.save()