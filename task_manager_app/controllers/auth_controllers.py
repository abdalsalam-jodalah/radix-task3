from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ValidationError

from task_manager_app.models.user_models import User
from rest_framework.exceptions import AuthenticationFailed
from ..models.user_device_models import UserDevice
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
            request_data = AuthComponents.fetch_headers_from_req(request)
            user_data = AuthComponents.fetch_login_data_from_req(request)
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

                    
        except UserDevice.DoesNotExist as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
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
        try:
            request_data = AuthComponents.fetch_headers_from_req(request)
            token = AuthComponents.fetch_token_from_req(request)
            user = AuthComponents.fetch_user_based_on_token(token)
            device_token = UserDeviceComponents.generate_device_id(
                user.id, request_data["device_name"], request_data["device_type"], request_data["user_agent"]
            )
            UserDeviceComponents.logout_device_based_on_token(device_token)
            AuthComponents.logout_user(user)
            AuthComponents.logout_token(token)
            logout(request)
            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        
        except UserDevice.DoesNotExist as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
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
