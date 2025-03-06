from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from ..models.user_device_models import UserDevice  
from ..components.auth_components import AuthComponents
from ..components.user_device_components import UserDeviceComponents

from rest_framework.response import Response

class IsSingleDevice(BasePermission):
    """
    Permission class to enforce single active device per user.
    """

    def has_permission(self, request, view):
        user_id = AuthComponents.extract_user_id_from_request(request)
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
        