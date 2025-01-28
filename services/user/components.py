from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  

class UserComponents():
    def get_all_users():
        return User.objects.all()

    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found!")

    def create_user(user_data):
        user = User(**user_data)
        user.save()

    def update_user(user_data):
        user = User.objects.get(id=user_data['id'])
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
    def authenticate_user(username, password,):
        try:
            user = User.objects.get(username=username)
            if not user.password.startswith('pbkdf2_'):
                user.password = make_password(user.password) 
                user.save()
        except User.DoesNotExist:
            return None
        if not user.check_password(password):
            return None
        
        return user