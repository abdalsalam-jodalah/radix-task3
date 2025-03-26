from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, ValidationError, NotAcceptable, AuthenticationFailed
from ..models.user_device_models import UserDevice  
from ..components.auth_components import AuthComponents
from ..components.user_device_components import UserDeviceComponents
from datetime import datetime, timezone
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from ..components.auth_components import AuthComponents
from ..components.user_components import UserComponents
from ..components.user_device_components import UserDeviceComponents
from ..models.user_models import User
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import logout

from rest_framework_simplejwt.exceptions  import TokenError
class IsSingleDeviceANDIsAuthenticatedAndUpdateStatus(BasePermission):
    """
    Enforces single active device per user. instead of deactivate token
    """
    def has_permission(self, request, view):
        try:
            valid_token = invalid_token = decoded_invalid_token = None
            try:
                valid_token = AuthComponents.fetch_token_from_req(request)
            except TokenError as err:
                if err.args:
                    error_info = err.args[0]
                    if isinstance(error_info, dict) and "token" in error_info:
                        invalid_token = error_info["token"]
                    else:
                        raise AuthenticationFailed("Invalid token.-")
                else:
                    raise AuthenticationFailed("Invalid token.--")    
            if invalid_token:
                decoded_invalid_token = AuthComponents.decode_expired_token(invalid_token)
                if not decoded_invalid_token:
                    raise AuthenticationFailed("Invalid token.---")
                user_id = decoded_invalid_token.get("user_id")
                user = UserComponents.get_user_by_id(user_id)
                valid_token = True

            if valid_token: 
                if not decoded_invalid_token:
                    user = AuthComponents.fetch_user_from_req(request)
                request_data = AuthComponents.fetch_headers_from_req(request)
                device_token = UserDeviceComponents.generate_device_id(
                    user.id, 
                    request_data["device_name"], 
                    request_data["device_type"], 
                    request_data["user_agent"]
                )
                device = UserDeviceComponents.fetch_device_by_user_and_token(user, device_token)
                
                if decoded_invalid_token:
                    UserDeviceComponents.logout_device_based_on_token(device_token)
                    AuthComponents.logout_user(user)
                    logout(request)
                    raise PermissionDenied("Token expired. Please log in again.")
                if device and device.is_active:
                    return True
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
