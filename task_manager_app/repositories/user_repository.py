from ..models.user_models import User
from ..models.role_models import Role
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger("repositories")

class UserRepository:
    @staticmethod
    def fetch_all_users():
        try:
            users = list(User.objects.all())
            return users
        except Exception as e:
            logger.error(f"fetch_all_users failed: {e}")
            raise Exception({"error": f"fetch_all_users failed: {e}"})

    @staticmethod
    def fetch_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            logger.info(f"fetch_user_by_id: User with id {user_id} not found")
            return None
        except Exception as e:
            logger.error(f"fetch_user_by_id failed for id {user_id}: {e}")
            raise Exception({"error": f"fetch_user_by_id failed for id {user_id}: {e}"})

    @staticmethod
    def fetch_user_by_email(email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            logger.info(f"fetch_user_by_email: User with email {email} not found")
            return None
        except Exception as e:
            logger.error(f"fetch_user_by_email failed for email {email}: {e}")
            raise Exception({"error": f"fetch_user_by_email failed for email {email}: {e}"})

    @staticmethod
    def filter_users_by_role(role):
        try:
            users = list(User.objects.filter(role=role))
            return users
        except Exception as e:
            logger.error(f"filter_users_by_role failed for role {role}: {e}")
            raise Exception({"error": f"filter_users_by_role failed for role {role}: {e}"})

    @staticmethod
    def filter_users_by_logging_status(is_logged_in):
        try:
            users = list(User.objects.filter(is_logged_in=is_logged_in))
            return users
        except Exception as e:
            logger.error(f"filter_user_by_logging_status failed for status {is_logged_in}: {e}")
            raise Exception({"error": f"filter_user_by_logging_status failed for status {is_logged_in}: {e}"})

    @staticmethod
    def create_user(user_data):
        try:
            user = User(**user_data)
            user.save()
            return user
        except Exception as e:
            logger.error(f"create_user failed: {e}")
            raise Exception({"error": f"create_user failed: {e}"})

    @staticmethod
    def update_user(user, user_data):
        try:
            for field, value in user_data.items():
                if field == "role":
                    value = Role.objects.get(id=int(value))
                if field == "parent":
                    value = User.objects.get(id=int(value))
                if field == "email" and user.email != user_data["email"]:
                    raise ValidationError({"email": "Email cannot be changed."})
                setattr(user, field, value)
            user.save()
            return user
        except Exception as e:
            logger.error(f"update_user failed for user id {user.id}: {e}")
            raise Exception({"error": f"update_user failed for user id {user.id}: {e}"})

    @staticmethod
    def delete_user(user):
        try:
            user.delete()
            return True
        except Exception as e:
            logger.error(f"delete_user failed for user id {user.id}: {e}")
            raise Exception({"error": f"delete_user failed for user id {user.id}: {e}"})

    @staticmethod
    def fetch_children(user):
        try:
            children = list(User.objects.filter(parent_id=user.id))
            return children
        except Exception as e:
            logger.error(f"fetch_children failed for user id {user.id}: {e}")
            raise Exception({"error": f"fetch_children failed for user id {user.id}: {e}"})

    @staticmethod
    def get_user_attribute(user, attr):
        try:
            return getattr(user, attr)
        except Exception as e:
            logger.error(f"get_user_attribute failed for user id {user.id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_user_attribute failed for user id {user.id}, attribute {attr}: {e}"})

    @staticmethod
    def set_user_attribute(user, attr, value):
        try:
            setattr(user, attr, value)
            user.save()
            return user
        except Exception as e:
            logger.error(f"set_user_attribute failed for user id {user.id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_user_attribute failed for user id {user.id}, attribute {attr}: {e}"})
