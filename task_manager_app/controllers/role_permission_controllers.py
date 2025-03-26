from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..permissions.user_permissions import IsSingleDeviceANDIsAuthenticatedAndUpdateStatus
from ..components.role_permission_components import RoleComponent, PermissionComponent
from ..serializers.role_serializers import RoleSerializer
from ..serializers.permission_serializers import  PermissionSerializer
from ..components.shared_components import SharedComponents
from ..serializers.role_permission_serailizers import RolePermissionSerializer
from ..components.role_permission_components import RolePermissionComponent
from ..pagination import CustomPagination
from ..decorators.handle_exceptions import handle_exceptions

import logging 
logger = logging.getLogger("controllers")

class RoleApi(APIView):
    authentication_classes = []
    permission_classes = [IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]
    pagination_class = CustomPagination
   
    @handle_exceptions   
    def get(self, request, pk=None):
        if pk:
            role = RoleComponent.get_role(pk)
            serializer = RoleSerializer(role)
        else:
            roles = RoleComponent.list_roles()
            serializer = RoleSerializer(roles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
   
    @handle_exceptions   
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            RoleComponent.create_role(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    @handle_exceptions   
    def put(self, request, pk):
        role = RoleComponent.update_role(pk, request.data)
        if role:
            serializer = RoleSerializer(role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

    @handle_exceptions   
    def delete(self, request, pk):
        if RoleComponent.delete_role(pk):
            return Response({"message": "Role deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


class PermissionApi(APIView):
    authentication_classes = []
    # permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    permission_classes = [ IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]
    pagination_class = CustomPagination
   
    @handle_exceptions   
    def get(self, request, pk=None):        
        if pk:
            permission = PermissionComponent.get_permission(pk)
            serializer = PermissionSerializer(permission)
            
        else:
            permissions = PermissionComponent.list_permissions()
            serializer = PermissionSerializer(permissions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @handle_exceptions   
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            PermissionComponent.create_permission(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    @handle_exceptions   
    def put(self, request, pk):
        role = RoleComponent.update_role(pk, request.data)
        if role:
            serializer = RoleSerializer(role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @handle_exceptions   
    def delete(self, request, pk):
        if RoleComponent.delete_role(pk):
            return Response({"message": "Role deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


class RolePermissionApi(APIView):
    authentication_classes = []
    # permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    permission_classes = [ IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]

    pagination_class = CustomPagination
   
    @handle_exceptions   
    def get(self, request, id=None):
        
        if id:
            rp = RolePermissionComponent.get_role_permission(id)
            if not rp:
                return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RolePermissionSerializer(rp)
        else:
            rps = RolePermissionComponent.list_role_permissions()
            serializer = RolePermissionSerializer(rps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    @handle_exceptions   
    def post(self, request):
        
            serializer = RolePermissionSerializer(data=request.data)
            if serializer.is_valid():
                rp = RolePermissionComponent.create_role_permission(serializer.validated_data)
                result_serializer = RolePermissionSerializer(rp)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    @handle_exceptions   
    def put(self, request, id):
        
            rp = RolePermissionComponent.update_role_permission(id, request.data)
            if rp:
                serializer = RolePermissionSerializer(rp)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
   
    @handle_exceptions   
    def delete(self, request, id):
        
            success = RolePermissionComponent.delete_role_permission(id)
            if success:
                return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "RolePermission not found"}, status=status.HTTP_404_NOT_FOUND)
