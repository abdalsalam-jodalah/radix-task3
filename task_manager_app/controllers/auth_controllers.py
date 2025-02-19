from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.auth_comopnents import AuthComponents
from ..components.shared_components import SharedComponents 
from ..components.user_components import UserComponents
from ..components.user_device_components import UserDeviceComponents 

import logging 

logger = logging.getLogger("views")

class AuthApi(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        return [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.method.lower() == "post":
    #         if "logout" in request.path:
    #             return self.log_out(request, *args, **kwargs)
    #         return self.sign_in(request, *args, **kwargs)  
    #     return super().dispatch(request, *args, **kwargs)

    renderer_classes = [JSONRenderer]
    authentication_classes = []

    def post(self, request):
        """Handles user login."""
        try:
            request_data = AuthComponents.fetch_user_request(request)
            request_data.update(AuthComponents.fetch_user_data(request))
            required_fields = ["email", "password", "device_name", "device_type", "user_agent"]

            if not all(request_data.get(field) for field in required_fields):
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "POST", None, additional_info="Missing required fields"
                ))
                return Response({"error": "Missing required fields in request."}, status=status.HTTP_400_BAD_REQUEST)

            user = AuthComponents.authenticate_user(email=request_data["email"], password=request_data["password"])
            if not user:
                logger.warning(SharedComponents.get_log_message(
                    "AuthApi", "POST", None, additional_info="Invalid login attempt"
                ))
                return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)

            data = AuthComponents.sign_user(user, request_data["device_name"], request_data["device_type"], request_data["user_agent"])

            if not data or "refresh" not in data or "access_token" not in data:
                logger.error(SharedComponents.get_log_message(
                    "AuthApi", "POST", data, additional_info="Token generation failed"
                ))

                return Response({"error": "Error signing user, invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(SharedComponents.get_log_message(
                "AuthApi", "POST", user, additional_info="User logged in successfully"
            ))


            return Response({
                'message': 'Login successful!',
                'access_token': data["access_token"],
                'refresh_token': str(data["refresh"])
            }, status=status.HTTP_200_OK)
        
        except AttributeError as err:
            logger.error(SharedComponents.get_log_message(
                    "AuthApi", "POST", None, additional_info=f"Error during login: {str(err)}"
            ))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))  
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_400_BAD_REQUEST)




    def put (self, request):
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
