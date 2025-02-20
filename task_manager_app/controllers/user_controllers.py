from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 

logger = logging.getLogger("views")


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
            return [IsAuthenticated(), IsSingleDevice()] 
        
    def get(self, request, user_id=None):
        """Retrieve a single user or list all users"""
        logger.debug(SharedComponents.get_log_message("UserApi", "GET", request.user, user_id, "User", "Fetching user(s)"))
        
        if user_id:
            user = UserComponents.get_user_by_id(user_id)
            if not user:
                logger.warning(SharedComponents.get_log_message("UserApi", "GET", request.user, user_id, "User", "User not found"))
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)   
            logger.info(SharedComponents.get_log_message("UserApi", "GET", request.user, user_id, "User", "User fetched successfully"))
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        
        users = UserComponents.get_all_users()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        logger.info(SharedComponents.get_log_message("UserApi", "GET", request.user, None, "User", f"Fetched {len(result_page)} users"))
        return paginator.get_paginated_response(UserSerializer(result_page, many=True).data)

    def post(self, request):
        """Create a new user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "POST", request.user, None, "User", "Creating new user"))
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserComponents.create_user(serializer.validated_data)
            if user:
                logger.info(SharedComponents.get_log_message("UserApi", "POST", request.user, user.id, "User", "User created successfully"))
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            
        logger.error(SharedComponents.get_log_message("UserApi", "POST", request.user, None, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        """Update an existing user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "Updating user"))

        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            UserComponents.update_user(serializer.validated_data)
            logger.info(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", "User updated successfully"))
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error(SharedComponents.get_log_message("UserApi", "PUT", request.user, user_id, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        """Partially update a user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "Partially updating user"))

        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            UserComponents.update_user(serializer.validated_data)
            logger.info(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", "User partially updated successfully"))
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.error(SharedComponents.get_log_message("UserApi", "PATCH", request.user, user_id, "User", f"Validation error: {serializer.errors}"))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Delete a user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "Deleting user"))

        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        logger.info(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User deleted successfully"))
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
