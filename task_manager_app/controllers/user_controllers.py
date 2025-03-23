from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.role_permission_components import RolePermissionComponent
logger = logging.getLogger("controllers")
from ..components.auth_components import AuthComponents
from ..models.user_models import User
from ..constants.role_constants import RoleChoices
from django.core.exceptions import ValidationError

class UserApi(APIView):
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        else:
            # return [IsAuthenticatedAndUpdateStatus(), IsSingleDevice()] 
            return [IsSingleDevice()] 

    def get(self, request, id=None):
        try:
            subject_user = AuthComponents.get_user(request)
            if not subject_user or not isinstance(subject_user, User):
                return Response({"error": "Invalid token, sign in again"}, status=status.HTTP_400_BAD_REQUEST)
                
            users = RolePermissionComponent.handle_action(subject_user, "user", "get")
            if not users:
                return Response({"error": "You don't have permissions"}, status=status.http)
            
            if id:
                user= UserComponents.get_user_from_users(users, id)
                if not user:
                    return Response({"error": "User not found!, or don't You have permissions"}, status=status.HTTP_404_NOT_FOUND)   
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(users, request)
            response = paginator.get_paginated_response(UserSerializer(result_page, many=True).data)

            return Response(response.data, status=status.HTTP_200_OK)
        
        except NotAcceptable as e:
            return Response({"error": f"Error: {e}"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"error": f"Error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            signup_data = AuthComponents.fetch_signup_data_from_req(request)
            signup_data.update({"role": RoleChoices.SUB_USER.value})
            UserComponents.validate_existing_user(signup_data)
            # user = RolePermissionComponent.handle_action(signup_data, "user", "post", request.data)
            # TODO: Fix the dispatcher since it take user object , but here we have data and want to make user obj
            user = UserComponents.create_user(signup_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """Update an existing user"""
        user_id =id
        if user_id == None:
            return Response({"error": "Missing user id, not found."}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "Updating user"))
        subject_user = AuthComponents.get_user(request)
        if not subject_user or not isinstance(subject_user, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        # user_to_edit = UserComponents.get_user_by_id(user_id)
        
        # if not user_to_edit:
        #     logger.warning(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User not found"))
        #     return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        # serializer = UserSerializer( data=request.data, partial=False)
        # if serializer.is_valid():
        result = RolePermissionComponent.handle_action(subject_user, "user", "put", request.data, user_id)
        if result == "User not found!":
            logger.warning(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User not found"))

            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User updated successfully"))
        return Response(request.data, status=status.HTTP_200_OK)

        logger.error(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        """Partially update a user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "Partially updating user"))
        subject_user = AuthComponents.get_user(request)
        if not subject_user or not isinstance(subject_user, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            UserComponents.update_user(serializer.validated_data,user_id)
            logger.info(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "User partially updated successfully"))
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.error(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Delete a user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "Deleting user"))
        subject_user = AuthComponents.get_user(request)
        if not subject_user or not isinstance(subject_user, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        logger.info(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User deleted successfully"))
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
