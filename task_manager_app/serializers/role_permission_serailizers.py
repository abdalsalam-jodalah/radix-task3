from rest_framework import serializers
from ..models.user_models import User
from .permission_serializers import PermissionSerializer
from .role_serializers import RoleSerializer

class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    permission = PermissionSerializer()

    class Meta:
        model = User
        fields = ['id', 'role', 'permission']