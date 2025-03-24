from rest_framework import serializers
import re
from ..serializers.user_device_serializers import UserDeviceSerializer
from ..serializers.task_serializers import TaskSerializer
from ..models.user_models import User
from ..models.user_device_models import UserDevice
from ..serializers.role_serializers import RoleSerializer
from ..models.role_models import Role
class UserSerializer(serializers.ModelSerializer):
    devices = serializers.PrimaryKeyRelatedField(many=True, queryset=UserDevice.objects.all(), required=False)
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(), slug_field="name"
    )
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_logged_in",
            "password",
            "created_at",
            "updated_at",
            "parent",
            "devices",
        ]
        extra_kwargs = {
            "email":     {"required": True},
            "password":  {"required": True, "write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "is_logged_in": {"required": False,"read_only": True},
            "updated_at": {"required": False,"read_only": True},
            "created_at": {"required": False,"read_only": True},
            "devices":{"required": False,"read_only": True},
        }

    def validate_email(self, value):
        if self.instance and self.instance.email != value:
            raise serializers.ValidationError({"email": "Email cannot be changed."})
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError({"email": "Enter a valid email address."})
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError({"password": "Password must contain at least one digit."})
        return value
    
