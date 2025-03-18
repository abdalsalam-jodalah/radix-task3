from django.core.exceptions import ValidationError
from ..models.user_models import User
from ..repositories.user_repository import UserRepository
from ..models.role_models import Role

class UserComponents:
    def get_all_users():
        return UserRepository.fetch_all_users()

    def get_user_by_id(user_id):
        try:
            return UserRepository.fetch_user_by_id(user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found!")
        
    def get_user_by_email(email):
        try:
            return UserRepository.fetch_user_by_email(email)
        except User.DoesNotExist:
            raise ValidationError("User not found!")

    def create_user(user_data):
        user_data["role"] = Role.objects.get(id=4)
        return UserRepository.create_user(user_data)
        
    def update_user(user_data,id):
        user = UserComponents.get_user_by_id(id)
        return UserRepository.update_user(user, user_data)

    def get_user_form_users(users, id):
        for user in users:
            if isinstance(user, dict) and user.get("id") == id:
                return user, {"message": "User found", "User": user}
            elif hasattr(user, "id") and user.id == id:
                return user, {"message": "User found", "User": user}
        return None, {"message": "User not found", "User": None}
    
    def assign_role():
        pass 
    
    def assign_parent():
        pass

    def get_own(user):
    
        return UserRepository.filter_user_by_id(user.id)

    def get_children(user):
        immediate_children = list(UserRepository.fetch_children(user))
    
        all_children = immediate_children.copy()

        for child in immediate_children:
            all_children.extend(UserComponents.get_children(child))
        return all_children

    def get_own_below(user):
    
        own = UserComponents.get_own(user)
    
        descendants = UserComponents.get_children(own.first())
    
        return [own.first()] + descendants

    def put_own(user, data, pk):
        if user.id != pk:
            raise ValidationError("You can only update your own profile.")
        user_instance = UserComponents.get_user_by_id(pk)
        return UserRepository.update_user(user_instance, data)

    def put_own_below(user, data, pk):
        if user.id == pk:
            return UserComponents.put_own(user, data, pk)
        
        descendants = UserComponents.get_own_below(user)
        if any(descendant.id == pk for descendant in descendants):
            user_instance = UserComponents.get_user_by_id(pk)
            return UserRepository.update_user(user_instance, data)
        else:
            raise ValidationError("You are not authorized to update this record.")

    def delete_user(user_id):
        user = UserComponents.get_user_by_id(user_id)
        return UserRepository.delete_user(user)
    def set_login_status(self, status: bool):
        self.is_logged_in = status
        self.save()
        # logger.info(f"User {self.email} login status updated to {status}")

