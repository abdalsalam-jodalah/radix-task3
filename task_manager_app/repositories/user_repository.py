from ..models.user_models import User
from ..models.role_models import Role
class UserRepository:
    def fetch_all_users():
        return User.objects.all()
    
    def fetch_user_by_id(user_id):
        return User.objects.get(id=user_id)
    
    def filter_user_by_id(user_id):
        return User.objects.filter(id=user_id)
    
    def fetch_user_by_email(email):
        return User.objects.get(email=email)
    
    def create_user(user_data):
        user = User(**user_data)
        user.save()
        return user
    
    def update_user(user, user_data):
        for field, value in user_data.items():
            if field == "role":
                value = Role.objects.get(id=int(value))
            if field == "parent":
                value = User.objects.get(id=int(value))
            setattr(user, field, value)
        user.save()
        return user


    def delete_user(user):
        user.delete()
        return True

    def fetch_children(user):
        return User.objects.filter(parent_id=user.id)