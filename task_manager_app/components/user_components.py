from django.core.exceptions import ValidationError
from ..models.user_models import User
from ..repositories.user_repository import UserRepository
from ..models.role_models import Role
import logging
from ..serializers.user_serializers import UserSerializer

logger = logging.getLogger("components")

class UserComponents:
    @staticmethod
    def get_all_users():
        try:
            return UserRepository.fetch_all_users()
        except Exception as e:
            logger.error(f"Error in get_all_users: {e}")
            raise Exception({"error": f"Error in get_all_users: {e}"})

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = UserRepository.fetch_user_by_id(user_id)
            if user is None:
                raise ValidationError({"error": "User not found!"})
            return user
        except Exception as e:
            logger.error(f"Error in get_user_by_id for id {user_id}: {e}")
            raise e

    @staticmethod
    def get_user_by_email(email):
        try:
            user = UserRepository.fetch_user_by_email(email)
            if user is None:
                raise ValidationError({"error": "User not found!"})
            return user
        except Exception as e:
            logger.error(f"Error in get_user_by_email for email {email}: {e}")
            raise e

    @staticmethod
    def create_user(user_data):
        try:
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid(raise_exception=True):
                new_user = serializer.save()
                return new_user
            return UserRepository.create_user(user_data)#not reached after adding serializer
        except Exception as e:
            logger.error(f"Error in create_user: {e}")
            raise e

    @staticmethod
    def update_user(user_data, user_id):
        try:
            user = UserComponents.get_user_by_id(user_id)
            return UserRepository.update_user(user, user_data)
        except Exception as e:
            logger.error(f"Error in update_user for user id {user_id}: {e}")
            raise e
    @staticmethod
    def validate_existing_user(signup_data):
        try:
            user = UserComponents.get_user_by_email(signup_data["email"])
            if user is not None:
                raise ValidationError({"error": "User with this email already exists!"})
        except ValidationError as e: # in case not found, its new user
            return None
        
    @staticmethod
    def get_user_from_users(users, user_id):
        try:
            for user in users:
                if isinstance(user, dict) and user.get("id") == user_id:
                    return user, {"message": "User found", "User": user}
                elif hasattr(user, "id") and user.id == user_id:
                    return user, {"message": "User found", "User": user}
            return None, {"message": "User not found", "User": None}
        except Exception as e:
            logger.error(f"Error in get_user_from_users: {e}")
            raise e

    @staticmethod
    def assign_role(user_id, role_id):
        try:
            user = UserComponents.get_user_by_id(user_id)
            role = Role.objects.get(id=role_id)
            return UserRepository.update_user(user, {"role": role.id})
        except Exception as e:
            logger.error(f"Error in assign_role for user id {user_id} and role id {role_id}: {e}")
            raise e

    @staticmethod
    def assign_parent(user_id, parent_id):
        try:
            user = UserComponents.get_user_by_id(user_id)
            parent = UserComponents.get_user_by_id(parent_id)
            if parent is None:
                raise ValidationError({"error": "Parent user not found!"})
            return UserRepository.update_user(user, {"parent": parent.id})
        except Exception as e:
            logger.error(f"Error in assign_parent for user id {user_id} with parent id {parent_id}: {e}")
            raise e

    @staticmethod
    def get_own(user):
        try:
            return UserRepository.fetch_user_by_id(user.id)
        except Exception as e:
            logger.error(f"Error in get_own for user id {user.id}: {e}")
            raise e

    @staticmethod
    def get_children(user):
        try:
            immediate_children = list(UserRepository.fetch_children(user))
            all_children = immediate_children.copy()
            for child in immediate_children:
                all_children.extend(UserComponents.get_children(child))
            return all_children
        except Exception as e:
            logger.error(f"Error in get_children for user id {user.id}: {e}")
            raise e

    @staticmethod
    def get_own_below(user):
        try:
            own = UserComponents.get_own(user)
            descendants = UserComponents.get_children(own)
            return [own] + descendants
        except Exception as e:
            logger.error(f"Error in get_own_below for user id {user.id}: {e}")
            raise e

    @staticmethod
    def put_own(user, data, pk):
        try:
            if user.id != pk:
                raise ValidationError({"error": "You can only update your own profile."})
            user_instance = UserComponents.get_user_by_id(pk)
            return UserRepository.update_user(user_instance, data)
        except Exception as e:
            logger.error(f"Error in put_own for user id {pk}: {e}")
            raise e

    @staticmethod
    def put_own_below(user, data, pk):
        try:
            if user.id == pk:
                return UserComponents.put_own(user, data, pk)
            descendants = UserComponents.get_own_below(user)
            if any(descendant.id == pk for descendant in descendants):
                user_instance = UserComponents.get_user_by_id(pk)
                return UserRepository.update_user(user_instance, data)
            else:
                raise ValidationError({"error": "You are not authorized to update this record."})
        except Exception as e:
            logger.error(f"Error in put_own_below for user id {pk}: {e}")
            raise e

    @staticmethod
    def delete_user(user_id):
        try:
            user = UserComponents.get_user_by_id(user_id)
            return UserRepository.delete_user(user)
        except Exception as e:
            logger.error(f"Error in delete_user for user id {user_id}: {e}")
            raise e

    def set_login_status(self, status: bool):
        try:
            self.is_logged_in = status
            self.save()
            return self
        except Exception as e:
            logger.error(f"Error in set_login_status for user id {self.id}: {e}")
            raise Exception({"error": f"Error in set_login_status for user id {self.id}: {e}"})
