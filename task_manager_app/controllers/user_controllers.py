from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..models.user_models import User
from ..components.user_components import UserComponents
from task_manager_app.pagination import CustomPagination

class UserApi(APIView):
    def get_permissions(self):
        """Return the permissions for the current request."""
        if self.request.method == 'POST':
            return [] 
        else:
            return [IsAuthenticated(), IsSingleDevice()] 
        
    def get(self, request, user_id=None):
        """Retrieve a single user or list all users"""
        if user_id:
            user = UserComponents.get_user_by_id(user_id)
            if not user:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        
        users = UserComponents.get_all_users()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(UserSerializer(result_page, many=True).data)

    def post(self, request):
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserComponents.create_user(serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        """Update an existing user"""
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            UserComponents.update_user(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        """Partially update a user"""
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            UserComponents.update_user(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """Delete a user"""
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
