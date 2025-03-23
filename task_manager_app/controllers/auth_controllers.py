from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ValidationError

from task_manager_app.models.user_models import User
from rest_framework.exceptions import AuthenticationFailed

from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.auth_components import AuthComponents
from ..components.shared_components import SharedComponents 
from ..components.user_components import UserComponents
from ..components.user_device_components import UserDeviceComponents 
from ..serializers.user_serializers import UserSerializer 
import logging 
logger = logging.getLogger("controllers")

class AuthApi(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        # return [IsAuthenticatedAndUpdateStatus(), IsSingleDevice()]
        return [ IsSingleDevice()]

    renderer_classes = [JSONRenderer]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """Handles both login and logout based on the request path."""
        if "logout" in request.path:
            return self.log_out(request, *args, **kwargs)
        return self.login(request, *args, **kwargs)
    
    def login(self, request, *args, **kwargs):
        try:
            request_data = AuthComponents.fetch_user_request(request)
            user_data = AuthComponents.fetch_user_data(request)
            request_data.update(user_data)

            user = AuthComponents.authenticate_user(email=request_data["email"], password=request_data["password"])
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

            tokens = AuthComponents.sign_user(user, request_data["device_name"], request_data["device_type"], request_data["user_agent"])

            if not tokens or "refresh_token" not in tokens or "access_token" not in tokens:
                return Response({"error": "Error signing user, invalid tokenization."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Login successful!',
                'access_token': tokens["access_token"],
                'refresh_token': tokens["refresh_token"],
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

                    
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)




    def log_out (self, request, *args, **kwargs):
        """Handles user logout from a single device."""
        logger.info("inside logout")

        try:
            request_data = AuthComponents.fetch_user_request(request)
            required_fields = ["device_name", "device_type", "user_agent", "auth_header"]

            if not all(request_data.get(field) for field in required_fields):
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "DELETE", request.user, additional_info="Missing required headers"
                ))
                return Response({"error": "Missing required headers."}, status=status.HTTP_400_BAD_REQUEST)

            token = AuthComponents.extract_token(request_data["auth_header"])
            if not token:
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "DELETE", request.user, additional_info="Token missing from request"
                ))
                return Response({"error": "User token not found."}, status=status.HTTP_400_BAD_REQUEST)

            user_id = AuthComponents.extract_user_id_from_auth_header(request_data["auth_header"])
            user = UserComponents.get_user_by_id(user_id)
            if not user:
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "DELETE", request.user, additional_info="User not found"
                ))
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

            device_identifier = UserDeviceComponents.generate_device_id(
                user_id, request_data["device_name"], request_data["device_type"], request_data["user_agent"]
            )
            if not device_identifier:
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "DELETE", request.user, additional_info="Device identification failed"
                ))
                return Response({"error": "Missing headers for device identification."}, status=status.HTTP_400_BAD_REQUEST)

            UserDeviceComponents.logout_device_basedon_token(device_identifier)
            AuthComponents.logout_user(user)
            AuthComponents.logout_token(token)
            logout(request)

            logger.info(SharedComponents.get_log_message(
                "AuthApi", "DELETE", user, additional_info="User logged out successfully"
            ))
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(SharedComponents.get_log_message(
                "AuthApi", "DELETE", request.user, additional_info=f"Error during logout: {str(e)}"
            ))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
