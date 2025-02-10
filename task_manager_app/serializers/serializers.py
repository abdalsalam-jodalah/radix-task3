from rest_framework import serializers
from ..models.user_models import User, UserDevice
from task_manager_app.serializers.task_serializers import TaskSerializer
import re

class UserDeviceSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source = 'user.id', read_only=True)
    class Meta:
        model =UserDevice
        fields = [
            "user_id",
            "device_name",
            "device_type",
            "device_token",
            "login_time",
            "logout_time",
            "is_active",
        ]

    def validate_device_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Device name must be at least 3 characters long!")
        return value

    # def validate_device_type(self, value):
    #     valid_types = ["mobile", "tablet", "laptop", "desktop"]
    #     if value.lower() not in valid_types:
    #         raise serializers.ValidationError(f"Device type must be one of {valid_types}!")
    #     return value

    def validate_device_token(self, value):
        if not value or len(value) < 20:
            raise serializers.ValidationError("Device token must be at least 20 characters long1")
        return value
    
    def validate_is_active(self, value):
        if value not in [True, False ]:
            raise serializers.ValidationError("Is active must be Boolean value!")
 
    def validate(self, attrs):
        login_time = attrs.get("login_time")
        logout_time = attrs.get("logout_time")
        if logout_time and login_time and logout_time <= login_time:
            raise serializers.ValidationError("Logout time must be later than login time!")
        return attrs
    
class UserSerializer(serializers.ModelSerializer):
    devices = UserDeviceSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'name', 
            'role', 
            'username', 
            'password',
            'devices',
            'is_logedin',
            'created_at',
            'updated_at',
            'tasks',
            ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_logedin': {'read_only': True},
            'updated_at' :{'read_only': True},
            'created_at' :{'read_only': True}
            }  


    def validate_username(self, value ):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address!")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long!")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter!")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter!")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit!")
        return value
    
    # def validate_isLoggedIn(self, value):
    #     if value not in [True,False]:
    #         raise serializers.ValidationError("")
    
    def validate_role(self, value):
        if value not in [choice[0] for choice in User.RoleChoices.choices]:
            raise serializers.ValidationError("Invalid role selected!")
        return value
    
