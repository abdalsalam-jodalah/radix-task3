from ..models.user_device_models import UserDevice
from django.core.exceptions import ValidationError
from ..models.user_models import User
import logging

logger = logging.getLogger("repositories")

class UserDeviceRepository:
    @staticmethod
    def fetch_all_devices():
        try:
            devices = list(UserDevice.objects.all())
            return devices
        except Exception as e:
            logger.error(f"fetch_all_devices failed: {e}")
            raise Exception({"error": f"fetch_all_devices failed: {e}"})

    @staticmethod
    def filter_devices_by_user(user):
        try:
            devices = list(UserDevice.objects.filter(user_id=user.id))
            return devices
        except Exception as e:
            logger.error(f"filter_devices_by_user failed for user id {user.id}: {e}")
            raise Exception({"error": f"filter_devices_by_user failed for user id {user.id}: {e}"})

    @staticmethod
    def filter_devices_by_active_status(is_active=True):
        try:
            devices = list(UserDevice.objects.filter(is_active=is_active))
            return devices
        except Exception as e:
            logger.error(f"filter_devices_by_active_status failed for is_active {is_active}: {e}")
            raise Exception({"error": f"filter_devices_by_active_status failed for is_active {is_active}: {e}"})

    @staticmethod
    def fetch_device_by_token(device_token):
        try:
            device = UserDevice.objects.filter(device_token=device_token).first()
            return device
        except Exception as e:
            logger.error(f"fetch_device_by_token failed for token {device_token}: {e}")
            raise Exception({"error": f"fetch_device_by_token failed for token {device_token}: {e}"})

    @staticmethod
    def create_device(user, device_token, is_active, login_time, logout_time):
        try:
            device = UserDevice.objects.create(
                user=user,
                device_token=device_token,
                is_active=is_active,
                login_time=login_time,
                logout_time=logout_time
            )
            
            return device
        except Exception as e:
            logger.error(f"create_device failed for user id {user.id}: {e}")
            raise Exception({"error": f"create_device failed for user id {user.id}: {e}"})

    @staticmethod
    def activate_device(existing_device, login_time, is_active=True, logout_time=None):
        try:
            if not isinstance(existing_device, UserDevice):
                raise ValidationError({"error": "Device not found or already logged out."})
            existing_device.is_active = is_active
            existing_device.login_time = login_time
            existing_device.logout_time = logout_time
            existing_device.save()
            return existing_device
        except ValidationError as ve:
            logger.error(f"activate_device validation error for device id {getattr(existing_device, 'id', 'N/A')}: {ve}")
            raise ValidationError({"error": f"activate_device validation error: {ve}"})
        except Exception as e:
            logger.error(f"activate_device failed for device id {getattr(existing_device, 'id', 'N/A')}: {e}")
            raise Exception({"error": f"activate_device failed for device id {getattr(existing_device, 'id', 'N/A')}: {e}"})

    @staticmethod
    def get_device_attribute(device, attr):
        try:
            return getattr(device, attr)
        except Exception as e:
            logger.error(f"get_device_attribute failed for device id {getattr(device, 'id', 'N/A')}, attribute {attr}: {e}")
            raise Exception({"error": f"get_device_attribute failed for device id {getattr(device, 'id', 'N/A')}, attribute {attr}: {e}"})

    @staticmethod
    def set_device_attribute(device, attr, value):
        try:
            setattr(device, attr, value)
            device.save()
            return device
        except Exception as e:
            logger.error(f"set_device_attribute failed for device id {getattr(device, 'id', 'N/A')}, attribute {attr}: {e}")
            raise Exception({"error": f"set_device_attribute failed for device id {getattr(device, 'id', 'N/A')}, attribute {attr}: {e}"})
