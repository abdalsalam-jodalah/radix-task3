from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['name', 'role', 'username', 'password','isLoggedIn']

    def validate_username(self, ):
        pass
    def validate_password(self, vlaue):
        pass
    def validate_isLoggedIn(self, vlaue):
        pass
    def validate_role(self, vlaue):
        pass
  
