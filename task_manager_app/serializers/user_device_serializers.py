from rest_framework import serializers
from ..models.user_device_mdoels import UserDevice

class UserDeviceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserDevice
        fields = [
            "user",
            "device_name",
            "device_type",
            "device_token",
            "login_time",
            "logout_time",
            "is_active",
        ]

    def validate_device_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Device name must be at least 3 characters long.")
        return value

    def validate_device_token(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Device token must be at least 20 characters long.")
        return value

    def validate(self, attrs):
        login_time = attrs.get("login_time")
        logout_time = attrs.get("logout_time")

        if logout_time and login_time and logout_time <= login_time:
            raise serializers.ValidationError("Logout time must be later than login time.")

        return super().validate(attrs)
