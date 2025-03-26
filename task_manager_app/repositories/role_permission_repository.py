from django.db import transaction
from ..models.role_models import Role
from ..models.permission_models import Permission
from ..models.role_permission_models import RolePermission
import logging

logger = logging.getLogger(__name__)

class RoleRepository:
    @staticmethod
    def get_all_roles():
        try:
            roles = list(Role.objects.all())
            return roles
        except Exception as e:
            logger.error(f"get_all_roles failed: {e}")
            raise Exception({"error": f"get_all_roles failed: {e}"})

    @staticmethod
    def get_role_by_id(id):
        try:
            role = Role.objects.filter(pk=id).first()
            return role
        except Exception as e:
            logger.error(f"get_role_by_id failed for role_id {id}: {e}")
            raise Exception({"error": f"get_role_by_id failed for role_id {id}: {e}"})

    @staticmethod
    def create_role(data):
        try:
            role = Role.objects.create(**data)
            return role
        except Exception as e:
            logger.error(f"create_role failed: {e}")
            raise Exception({"error": f"create_role failed: {e}"})

    @staticmethod
    def update_role(role, data):
        try:
            for key, value in data.items():
                setattr(role, key, value)
            role.save()
            return role
        except Exception as e:
            role_id = getattr(role, 'id', 'N/A')
            logger.error(f"update_role failed for role id {role_id}: {e}")
            raise Exception({"error": f"update_role failed for role id {role_id}: {e}"})

    @staticmethod
    def delete_role(role):
        try:
            role.delete()
            return role
        except Exception as e:
            role_id = getattr(role, 'id', 'N/A')
            logger.error(f"delete_role failed for role id {role_id}: {e}")
            raise Exception({"error": f"delete_role failed for role id {role_id}: {e}"})

    @staticmethod
    def get_role_attribute(role, attr):
        try:
            return getattr(role, attr)
        except Exception as e:
            role_id = getattr(role, 'id', 'N/A')
            logger.error(f"get_role_attribute failed for role id {role_id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_role_attribute failed for role id {role_id}, attribute {attr}: {e}"})

    @staticmethod
    def set_role_attribute(role, attr, value):
        try:
            setattr(role, attr, value)
            role.save()
            return role
        except Exception as e:
            role_id = getattr(role, 'id', 'N/A')
            logger.error(f"set_role_attribute failed for role id {role_id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_role_attribute failed for role id {role_id}, attribute {attr}: {e}"})


class PermissionRepository:
    @staticmethod
    def get_all_permissions():
        try:
            permissions = list(Permission.objects.all())
            return permissions
        except Exception as e:
            logger.error(f"get_all_permissions failed: {e}")
            raise Exception({"error": f"get_all_permissions failed: {e}"})

    @staticmethod
    def get_permission_by_id(permission_id):
        try:
            permission = Permission.objects.filter(pk=permission_id).first()
            return permission
        except Exception as e:
            logger.error(f"get_permission_by_id failed for permission_id {permission_id}: {e}")
            raise Exception({"error": f"get_permission_by_id failed for permission_id {permission_id}: {e}"})

    @staticmethod
    def create_permission(data):
        try:
            permission = Permission.objects.create(**data)
            return permission
        except Exception as e:
            logger.error(f"create_permission failed: {e}")
            raise Exception({"error": f"create_permission failed: {e}"})

    @staticmethod
    def update_permission(permission, data):
        try:
            for key, value in data.items():
                setattr(permission, key, value)
            permission.save()
            return permission
        except Exception as e:
            perm_id = getattr(permission, 'id', 'N/A')
            logger.error(f"update_permission failed for permission id {perm_id}: {e}")
            raise Exception({"error": f"update_permission failed for permission id {perm_id}: {e}"})

    @staticmethod
    def delete_permission(permission):
        try:
            permission.delete()
            return permission
        except Exception as e:
            perm_id = getattr(permission, 'id', 'N/A')
            logger.error(f"delete_permission failed for permission id {perm_id}: {e}")
            raise Exception({"error": f"delete_permission failed for permission id {perm_id}: {e}"})

    @staticmethod
    def get_permission_attribute(permission, attr):
        try:
            return getattr(permission, attr)
        except Exception as e:
            perm_id = getattr(permission, 'id', 'N/A')
            logger.error(f"get_permission_attribute failed for permission id {perm_id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_permission_attribute failed for permission id {perm_id}, attribute {attr}: {e}"})

    @staticmethod
    def set_permission_attribute(permission, attr, value):
        try:
            setattr(permission, attr, value)
            permission.save()
            return permission
        except Exception as e:
            perm_id = getattr(permission, 'id', 'N/A')
            logger.error(f"set_permission_attribute failed for permission id {perm_id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_permission_attribute failed for permission id {perm_id}, attribute {attr}: {e}"})


class RolePermissionRepository:
    @staticmethod
    def get_permissions_by_role(role):
        try:
            role_permissions = list(RolePermission.objects.filter(role=role))
            return role_permissions
        except Exception as e:
            logger.error(f"get_permissions_by_role failed for role id {role.id}: {e}")
            raise Exception({"error": f"get_permissions_by_role failed for role id {role.id}: {e}"})

    @staticmethod
    def list_role_permissions():
        try:
            role_permissions = list(RolePermission.objects.select_related('role', 'permission').all())
            return role_permissions
        except Exception as e:
            logger.error(f"list_role_permissions failed: {e}")
            raise Exception({"error": f"list_role_permissions failed: {e}"})

    @staticmethod
    def get_role_permission(pk):
        try:
            role_permission = RolePermission.objects.select_related('role', 'permission').get(pk=pk)
            return role_permission
        except RolePermission.DoesNotExist:
            logger.info(f"get_role_permission: RolePermission with pk {pk} not found")
            return None
        except Exception as e:
            logger.error(f"get_role_permission failed for pk {pk}: {e}")
            raise Exception({"error": f"get_role_permission failed for pk {pk}: {e}"})

    @staticmethod
    def create_role_permission(data):
        try:
            with transaction.atomic():
                role = Role.objects.get(pk=data.get('role_id'))
                permission = Permission.objects.get(pk=data.get('permission_id'))
                rp = RolePermission.objects.create(role=role, permission=permission)
                return rp
        except Exception as e:
            logger.error(f"create_role_permission failed: {e}")
            raise Exception({"error": f"create_role_permission failed: {e}"})

    @staticmethod
    def update_role_permission(pk, data):
        try:
            with transaction.atomic():
                rp = RolePermission.objects.get(pk=pk)
                if 'role_id' in data:
                    role = Role.objects.get(pk=data.get('role_id'))
                    rp.role = role
                if 'permission_id' in data:
                    permission = Permission.objects.get(pk=data.get('permission_id'))
                    rp.permission = permission
                rp.save()
                return rp
        except RolePermission.DoesNotExist:
            logger.info(f"update_role_permission: RolePermission with pk {pk} not found")
            return None
        except Exception as e:
            logger.error(f"update_role_permission failed for pk {pk}: {e}")
            raise Exception({"error": f"update_role_permission failed for pk {pk}: {e}"})

    @staticmethod
    def delete_role_permission(pk):
        try:
            rp = RolePermission.objects.get(pk=pk)
            rp.delete()
            return True
        except RolePermission.DoesNotExist:
            logger.info(f"delete_role_permission: RolePermission with pk {pk} not found")
            return False
        except Exception as e:
            logger.error(f"delete_role_permission failed for pk {pk}: {e}")
            raise Exception({"error": f"delete_role_permission failed for pk {pk}: {e}"})

    @staticmethod
    def get_role_permission_attribute(rp, attr):
        try:
            return getattr(rp, attr)
        except Exception as e:
            rp_id = getattr(rp, 'id', 'N/A')
            logger.error(f"get_role_permission_attribute failed for rp id {rp_id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_role_permission_attribute failed for rp id {rp_id}, attribute {attr}: {e}"})

    @staticmethod
    def set_role_permission_attribute(rp, attr, value):
        try:
            setattr(rp, attr, value)
            rp.save()
            return rp
        except Exception as e:
            rp_id = getattr(rp, 'id', 'N/A')
            logger.error(f"set_role_permission_attribute failed for rp id {rp_id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_role_permission_attribute failed for rp id {rp_id}, attribute {attr}: {e}"})
