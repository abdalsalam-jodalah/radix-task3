from rest_framework import serializers
from ..models.permission_models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
