import hashlib
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from ..repositories.user_device_repository import UserDeviceRepository
from ..models.user_device_models import UserDevice
from ..models.user_models import User
import logging

logger = logging.getLogger("components")

class UserDeviceComponents:
    @staticmethod
    def generate_device_id(user_id, device_name, device_type, user_agent):
        if not device_name or not device_type or not user_agent:
            raise ValidationError({"error": "Device name, device type, and user agent are required."})
        separator = "::"
        raw_data = f"{user_id}{separator}{device_name}{separator}{device_type}{separator}{user_agent}"
        if not raw_data:
            raise ValidationError({"error": "Device data is required."})
        return raw_data

    @staticmethod
    def fetch_device_by_user_and_token(user, device_token):
        try:
            devices = UserDeviceRepository.filter_devices_by_user(user)
            for device in devices:
                if device.device_token == device_token:
                    return device
            return None
        except Exception as e:
            logger.error(f"fetch_device_by_user_and_token failed for user {user.id}: {e}")
            raise Exception({"error": f"fetch_device_by_user_and_token failed for user {user.id}: {e}"})

    @staticmethod
    def authenticate_device(user, existing_device):
        try:
            if existing_device:
                if existing_device.is_active:
                    return  "exist_active"
                else:
                    return "exist_not_active"
            else:
                return "not_exist"
        except Exception as err:
            logger.error(f"authenticate_device error for user {user.id}: {err}")
            return "not_exist"

    @staticmethod
    def register_device(user, existing_device, device_token, status):
        try:
            if status == "exist_not_active" or "exist_active" and existing_device:
                activated_device = UserDeviceRepository.activate_device(existing_device, now(), True, None)
                return activated_device
            elif status == "not_exist":
                print(f"status: {status}, existing_device: {existing_device}, user: {user}, device_token: {device_token}")
                new_device = UserDeviceRepository.create_device(user, device_token, True, now(), None)
                return new_device
            else:
                raise ValidationError({"error": "Invalid status provided for device registration."})
        except Exception as e:
            logger.error(f"register_device error for user {user.id}: {e}")
            raise Exception({"error": f"register_device error for user {user.id}: {e}"})

    @staticmethod
    def logout_device_based_on_token(device_identifier):
        try:
            device = UserDeviceRepository.fetch_device_by_token(device_identifier)
            if device is None:
                raise ValidationError({"error": "Device not found or already logged out."})
            return UserDeviceComponents.logout_device(device)
        except Exception as e:
            logger.error(f"logout_device_based_on_token error for token {device_identifier}: {e}")
            raise Exception({"error": f"logout_device_based_on_token error for token {device_identifier}: {e}"})

    @staticmethod
    def logout_all_devices_for_user(user):
        try:
            devices = UserDeviceRepository.filter_devices_by_user(user)
            for device in devices:
                UserDeviceComponents.logout_device(device)
            return {"message": "All devices logged out."}
        except Exception as e:
            logger.error(f"logout_all_devices_for_user error for user {user.id}: {e}")
            raise Exception({"error": f"logout_all_devices_for_user error for user {user.id}: {e}"})

    @staticmethod
    def logout_device(device):
        try:
            if isinstance(device, UserDevice):
                UserDeviceRepository.set_device_attribute(device, 'is_active', False)
                UserDeviceRepository.set_device_attribute(device, 'logout_time', now())
                return device
            else:
                raise ValidationError({"error": "Device not found or already logged out."})
        except Exception as e:
            logger.error(f"logout_device error for device id {getattr(device, 'id', 'N/A')}: {e}")
            raise Exception({"error": f"logout_device error for device id {getattr(device, 'id', 'N/A')}: {e}"})
