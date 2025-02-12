from django.core.exceptions import ValidationError
from ..models.user_models import User

class UserComponents():
    def get_all_users():
        return User.objects.all()

    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found!")
        
    def get_user_by_username(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("User not found!")

    def create_user(user_data):
        user = User(**user_data)
        user.save()

    def update_user(user_data):
        user = UserComponents.get_user_by_id(user_data['id'])
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
