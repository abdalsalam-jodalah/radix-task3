from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.role_permission_components import RolePermissionComponent
logger = logging.getLogger("views")
from ..components.auth_comopnents import AuthComponents as AC
from ..models.user_models import User

class UserApi(APIView):
    """
    Handles CRUD operations for User.
    """
    pagination_class = CustomPagination

    def get_permissions(self):
        """Return the permissions for the current request."""
        if self.request.method == 'POST':
            return [] 
        else:
            return [IsAuthenticatedAndUpdateStatus(), IsSingleDevice()] 
        
    def get(self, request, id=None):
        logger.debug(SharedComponents.get_log_message("UserApi", "GET", request.user, id, "User", "Fetching user(s)"))
        user_subject = AC.get_user(request)
        if not user_subject or not isinstance(user_subject, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        result = RolePermissionComponent.handle_action(user_subject, "user", "get")
        users = result      
        if id:
            user= UserComponents.get_user_form_users(users, id)
            if not user:
                logger.warning(SharedComponents.get_log_message("UserApi", "GET", request.user, id, "User", "User not found"))
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)   
            logger.info(SharedComponents.get_log_message("UserApi", "GET", request.user, id, "User", "User fetched successfully"))
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            
        
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        logger.info(SharedComponents.get_log_message("UserApi", "GET", request.user, None, "User", f"Fetched {len(result_page)} users"))
        return paginator.get_paginated_response(UserSerializer(result_page, many=True).data)

    def post(self, request):
        """Create a new user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "POST", request.user, None, "User", "Creating new user"))
        user_subject = AC.get_user(request)
        if not user_subject or not isinstance(user_subject, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user= RolePermissionComponent.handle_action(user_subject, "user", "post",request.data)
            if user:
                logger.info(SharedComponents.get_log_message("UserApi", "POST", request.user, user.id, "User", "User created successfully"))
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            
        logger.error(SharedComponents.get_log_message("UserApi", "POST", request.user, None, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        """Update an existing user"""
        user_id =id
        if user_id == None:
            return Response({"error": "Missing user id, not found."}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "Updating user"))
        user_subject = AC.get_user(request)
        if not user_subject or not isinstance(user_subject, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        # user_to_edit = UserComponents.get_user_by_id(user_id)
        
        # if not user_to_edit:
        #     logger.warning(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User not found"))
        #     return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        # serializer = UserSerializer( data=request.data, partial=False)
        # if serializer.is_valid():
        result = RolePermissionComponent.handle_action(user_subject, "user", "put", request.data, user_id)
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
        user_subject = AC.get_user(request)
        if not user_subject or not isinstance(user_subject, User):
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
        user_subject = AC.get_user(request)
        if not user_subject or not isinstance(user_subject, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        logger.info(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User deleted successfully"))
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
