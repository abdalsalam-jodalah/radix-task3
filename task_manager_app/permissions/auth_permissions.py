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

class IsAuthenticatedAndUpdateStatus(BasePermission):
    """
    Custom permission to check authentication and update the user's login status when token expires.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return False  

        try:
            print("000")
            decoded_token = AuthComponents.decode_expired_token(auth_header)
            print("111")
            if not decoded_token:
                raise AuthenticationFailed("Invalid token.")
            print("222")
            exp_timestamp = decoded_token.get('exp')
            if not exp_timestamp:
                raise AuthenticationFailed("Token has no expiration.")
            print("333")

            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            print("444")
            if exp_datetime < now():

                user_id = decoded_token.get("user_id")
                if not user_id:
                    raise AuthenticationFailed("Token does not contain user ID.")
                print("555")
                user = UserComponents.get_user_by_id(user_id)

                if not user or not  isinstance(user, User):
                    raise AuthenticationFailed("Token does not contain user ID.")
                print("666")
                AuthComponents.logout_user(user)  
                UserDeviceComponents.logout_all_devices_for_user(user)
                print("777")

                raise AuthenticationFailed("Token expired, user logged out.")

            return True  

        except Exception as err:
            print(f"Exception: {err}")
            return Response({"detail": "logged out, please log in again."}, status=status.HTTP_400_BAD_REQUEST)
            return False  
