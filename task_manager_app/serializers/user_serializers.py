from rest_framework import serializers
import re
from ..serializers.user_device_serializers import UserDeviceSerializer
from ..serializers.task_serializers import TaskSerializer
from ..models.user_models import User
from ..serializers.role_serializers import RoleSerializer
from ..models.role_models import Role
class UserSerializer(serializers.ModelSerializer):
    devices = UserDeviceSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset= Role.objects.all())  
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "role",
            "is_logged_in",
            "email",
            "password",
            "devices",
            "tasks",
            "created_at",
            "updated_at",
            'role',
            "parent"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_logged_in": {"read_only": True},
            "updated_at": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def validate_email(self, value):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    # def validate_role(self, value):
    #     if value not in [choice[0] for choice in User.RoleChoices.choices]:
    #         raise serializers.ValidationError("Invalid role selected.")
    #     return value
