from rest_framework.permissions import BasePermission
from ..components.auth_comopnents import AuthComponents
from ..components.user_components import UserComponents
from ..components.role_permission_components import RolePermissionComponent

class HasRolePermission(BasePermission):
    def has_permission(self, request, view):

        required_permissions = getattr(view, "permission_required", None)
        if not required_permissions:
            return True  
        
        userId = AuthComponents.extract_user_id_from_request(request)
        user = UserComponents.get_user_by_id(userId)
        user_role = user.role 
        user_permissions = RolePermissionComponent.get_permissions_by_role(user_role)
        permission_names = [permission.name for permission in user_permissions]
        
        if user_role == "Admin":
            return True
        return all(perm in user_permissions for perm in required_permissions) if isinstance(required_permissions, list) else required_permissions in user_permissions

        if isinstance(required_permissions, list):
            return all(perm in permission_names for perm in required_permissions)
        return required_permissions in permission_names
    
        if user_role == "Manager":
            return self.check_manager_permissions(required_permissions, permission_names)
        elif user_role == "User":
            return self.check_user_permissions(required_permissions, permission_names)
        elif user_role == "Sub-User":
            return self.check_sub_user_permissions(required_permissions, permission_names)
        return False

    def check_manager_permissions(self, required_permission, permission_names):
        manager_permissions = RolePermissionComponent.get_permissions_by_role("Manager")
        if isinstance(required_permission, list):  
            return all(perm in permission_names for perm in required_permission)
        else:
            return required_permission in manager_permissions and required_permission in permission_names

    def check_user_permissions(self, required_permission, permission_names):
        user_permissions = RolePermissionComponent.get_permissions_by_role("User")

        if isinstance(required_permission, list): 
            return all(perm in permission_names for perm in required_permission)
        else:
            return required_permission in user_permissions and required_permission in permission_names

    def check_sub_user_permissions(self, required_permission, permission_names):
        sub_user_permissions = RolePermissionComponent.get_permissions_by_role("Sub-User")
        
        if isinstance(required_permission, list):  
            return all(perm in permission_names for perm in required_permission)
        else:
            return required_permission in sub_user_permissions and required_permission in permission_names
