from django.core.exceptions import ValidationError
from ..models.user_models import User
from ..repositories.user_repository import UserRepository

class UserComponents():
    def get_all_users():
        return UserRepository.fetch_all_users()

    def get_user_by_id(user_id):
        try:
            return UserRepository.fetch_user_by_id(user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found!")
        
    def get_user_by_username(username):
        try:
            return UserRepository.fetch_user_by_username
        except User.DoesNotExist:
            raise ValidationError("User not found!")

    def create_user(user_data):
        UserRepository.create_user(user_data)
        

    def update_user(user_data):
        user = UserComponents.get_user_by_id(user_data['id'])
        UserRepository.update_user(user, user_data)