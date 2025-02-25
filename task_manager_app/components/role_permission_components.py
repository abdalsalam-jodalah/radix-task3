from ..repositories.role_permission_repository import RoleRepository, PermissionRepository
from ..repositories.role_permission_repository import RolePermissionRepository
from django.apps import apps

class RoleComponent:
    def list_roles():
        return RoleRepository.get_all_roles()

    def get_role(role_id):
        return RoleRepository.get_role_by_id(role_id)

    def create_role(data):
        return RoleRepository.create_role(data)

    def update_role(role_id, data):
        role = RoleRepository.get_role_by_id(role_id)
        if role:
            return RoleRepository.update_role(role, data)
        return None

    def delete_role(role_id):
        role = RoleRepository.get_role_by_id(role_id)
        if role:
            RoleRepository.delete_role(role)
            return True
        return False


class PermissionComponent:
    def list_permissions():
        return PermissionRepository.get_all_permissions()

    def get_permission(permission_id):
        return PermissionRepository.get_permission_by_id(permission_id)

    def create_permission(data):
        return PermissionRepository.create_permission(data)

    def update_permission(permission_id, data):
        permission = PermissionRepository.get_permission_by_id(permission_id)
        if permission:
            return PermissionRepository.update_permission(permission, data)
        return None

    def delete_permission(permission_id):
        permission = PermissionRepository.get_permission_by_id(permission_id)
        if permission:
            PermissionRepository.delete_permission(permission)
            return True
        return False
    
class RolePermissionComponent:
    # def add_permission_to_role(role, permission):
    #     role.permissions.add(permission)
    #     return role

    # def remove_permission_from_role(role, permission):
    #     role.permissions.remove(permission)
    #     return role
    
    def get_permissions_by_role(role):
        return RolePermissionRepository.get_permissions_by_role(role)




    # def get_role_permissions(role_name):
    #     """Fetch role permissions dynamically from the database."""
    #     try:
    #         role = Role.objects.prefetch_related("permissions").get(name=role_name)
    #         return set(role.permissions.values_list("name", flat=True))
    #     except Role.DoesNotExist:
    #         return set()

    def get_role_actions(user, model_name):
        """Dynamically map role permissions to CRUD operations for any model"""
        # permissions = get_role_permissions(user.role.name if user.role else "Guest")
        permissions = RolePermissionComponent.get_permissions_by_role(user.role.name if user.role else "Guest")

        Model = apps.get_model('task_manager_app', model_name)

        return {
            "get": lambda: Model.objects.all() if f"view_all_{model_name.lower()}" in permissions else Model.objects.filter(user=user),
            "create": lambda data: Model.objects.create(**data) if f"create_{model_name.lower()}" in permissions else None,
            "update": lambda instance, data: instance.update(**data) if f"edit_{model_name.lower()}" in permissions else None,
            "delete": lambda instance: instance.delete() if f"delete_{model_name.lower()}" in permissions else None,
        }
