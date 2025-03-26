from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, ValidationError, NotAcceptable, AuthenticationFailed
from ..models.user_device_models import UserDevice  
from ..components.auth_components import AuthComponents
from ..components.user_device_components import UserDeviceComponents

class IsSingleDevice(BasePermission):
    """
    Enforces single active device per user. instead of deactivate token
    """
    def has_permission(self, request, view):
        try:
            user = AuthComponents.fetch_user_from_req(request)
            request_data = AuthComponents.fetch_headers_from_req(request)
            device_token = UserDeviceComponents.generate_device_id(
                user.id, 
                request_data["device_name"], 
                request_data["device_type"], 
                request_data["user_agent"]
            )
            device = UserDeviceComponents.fetch_device_by_user_and_token(user, device_token)
            
            if device and device.is_active:
                return True
            print(  "device", device)
            raise PermissionDenied("Session expired or u logged in from other Device. Please log in again.")
        except PermissionDenied as err:
            raise PermissionDenied({"error": str(err)})   
        except UserDevice.DoesNotExist as err:
            raise PermissionDenied({"error": f"Device not registered. Please log in again. Err: {err}"})
        except ValueError as err:
            raise ValidationError({"error": str(err)})
        except NotAcceptable as err:
            raise NotAcceptable({"error": str(err)})
        except AuthenticationFailed as err:
            raise AuthenticationFailed({"error": str(err)})
        except Exception as e:
            raise PermissionDenied({"error": f"An unexpected error occurred: {e}"})
