from rest_framework import serializers
import re
from ..serializers.user_device_serializers import UserDeviceSerializer
from ..serializers.task_serializers import TaskSerializer
from ..models.user_models import User

class UserSerializer(serializers.ModelSerializer):
    devices = UserDeviceSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "role",
            "is_logedin",
            "username",
            "password",
            "devices",
            "tasks",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_logedin": {"read_only": True},
            "updated_at": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def validate_username(self, value):
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

    def validate_role(self, value):
        if value not in [choice[0] for choice in User.RoleChoices.choices]:
            raise serializers.ValidationError("Invalid role selected.")
        return value
