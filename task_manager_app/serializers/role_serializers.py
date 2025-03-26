from rest_framework import serializers
from ..models.role_models import Role
from .permission_serializers import PermissionSerializer

class RoleSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'permission']    
