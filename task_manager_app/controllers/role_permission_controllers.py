from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.role_permission_components import RoleComponent, PermissionComponent
from ..serializers.role_serializers import RoleSerializer
from ..serializers.permission_serializers import  PermissionSerializer
from ..components.shared_components import SharedComponents
from ..serializers.role_permission_serailizers import RolePermissionSerializer
from ..components.role_permission_components import RolePermissionComponent
from ..pagination import CustomPagination

import logging 
logger = logging.getLogger("views")

class RoleApi(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        try:
            if pk:
                role = RoleComponent.get_role(pk)
                serializer = RoleSerializer(role)
            else:
                roles = RoleComponent.list_roles()
                serializer = RoleSerializer(roles, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "GET", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                RoleComponent.create_role(serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "POST", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            role = RoleComponent.update_role(pk, request.data)
            if role:
                serializer = RoleSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "PUT", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            if RoleComponent.delete_role(pk):
                return Response({"message": "Role deleted"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "DELETE", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionApi(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        try:
            if pk:
                permission = PermissionComponent.get_permission(pk)
                serializer = PermissionSerializer(permission)
            else:
                permissions = PermissionComponent.list_permissions()
                serializer = PermissionSerializer(permissions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            SharedComponents.log_error("PermissionApi", "GET", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = PermissionSerializer(data=request.data)
            if serializer.is_valid():
                PermissionComponent.create_permission(serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            SharedComponents.log_error("PermissionApi", "POST", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        try:
            role = RoleComponent.update_role(pk, request.data)
            if role:
                serializer = RoleSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "PUT", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        try:
            if RoleComponent.delete_role(pk):
                return Response({"message": "Role deleted"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RoleApi", "DELETE", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RolePermissionApi(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request, id=None):
        try:
            if id:
                rp = RolePermissionComponent.get_role_permission(id)
                if not rp:
                    return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
                serializer = RolePermissionSerializer(rp)
            else:
                rps = RolePermissionComponent.list_role_permissions()
                serializer = RolePermissionSerializer(rps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            SharedComponents.log_error("RolePermissionApi", "GET", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = RolePermissionSerializer(data=request.data)
            if serializer.is_valid():
                rp = RolePermissionComponent.create_role_permission(serializer.validated_data)
                result_serializer = RolePermissionSerializer(rp)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            SharedComponents.log_error("RolePermissionApi", "POST", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            rp = RolePermissionComponent.update_role_permission(id, request.data)
            if rp:
                serializer = RolePermissionSerializer(rp)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RolePermissionApi", "PUT", e)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            success = RolePermissionComponent.delete_role_permission(id)
            if success:
                return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            SharedComponents.log_error("RolePermissionApi", "DELETE", e)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
