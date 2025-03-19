from rest_framework import serializers
from ..models.user_device_models import UserDevice

class UserDeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserDevice
        fields = [
            "user",
            "device_token",
            "login_time",
            "logout_time",
            "is_active",
        ]
        extra_kwargs = {
            "user": {"required": True},
            "device_token": {"required": True},
            "login_time": {"required": False,"read_only": True},
            "logout_time": {"required": False,"read_only": True},
            "is_active": {"required": False, "read_only": True},
        }
