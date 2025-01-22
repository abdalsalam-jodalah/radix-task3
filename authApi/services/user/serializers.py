from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 
            'role', 
            'username', 
            'password',
            'isLoggedIn', 
            'last_login_from'
            ]
        extra_kwargs = {
            'password': {'write_only': True},
            'isLoggedIn':{'read_only': True}
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
    
    def validate_isLoggedIn(self, value):
        if value not in [True,False]:
            raise serializers.ValidationError("")
    
    def validate_role(self, value):
        if value not in [choice[0] for choice in User.RoleChoices.choices]:
            raise serializers.ValidationError("Invalid role selected!")
        return value
    
