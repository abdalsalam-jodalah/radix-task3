from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import UserDevice  
from .components import UserComponents,UserDeviceComponents
from rest_framework.response import Response

class IsSingleDevice(BasePermission):
    """
    Permission class to enforce single active device per user.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization") 
        user_id = UserComponents.extract_user_id_from_auth_header(auth_header)
        if not user_id:
            raise PermissionDenied({"error": "user id not founded in header."})
        
        device_name = request.headers.get('Sec-Ch-Ua-Platform', 'Unknown Device')
        device_type = request.headers.get('Sec-Ch-Ua', 'Unknown Device')
        user_agent = request.headers.get('User-Agent', 'Unknown User Agent')

        device_identifier = UserDeviceComponents.generate_device_id(user_id, device_name, device_type, user_agent)

        try:
            device = UserDevice.objects.get(device_token=device_identifier)
            if not device.is_active:
                raise PermissionDenied({"error": "Session expired. Please log in again from this device."})
            return True
        except UserDevice.DoesNotExist:
            raise PermissionDenied({"error": "Device not registered. Please log in again."})
        