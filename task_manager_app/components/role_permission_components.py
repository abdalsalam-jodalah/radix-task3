from django.apps import apps
from rest_framework.exceptions import NotAcceptable
import importlib

from ..repositories.role_permission_repository import RoleRepository, PermissionRepository
from ..repositories.role_permission_repository import RolePermissionRepository
from ..dispatchers.base_dispatcher import  BaseDispatcher
from ..models.permission_models import Permission 
from ..models.role_permission_models import RolePermission

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
    def get_permissions_by_role(role):
        return RolePermissionRepository.get_permissions_by_role(role)

    def get_role_permissions(role):
        if not role:
            return set()
        return {perm.name for perm in role.permissions.all()}  
    def list_role_permissions():
        return RolePermissionRepository.list_role_permissions()

    def get_role_permission(pk):
        return RolePermissionRepository.get_role_permission(pk)

    def create_role_permission(data):
        return RolePermissionRepository.create_role_permission(data)

    def update_role_permission(pk, data):
        return RolePermissionRepository.update_role_permission(pk, data)

    def delete_role_permission(pk):
        return RolePermissionRepository.delete_role_permission(pk)  

    def get_permissions_by_role_decoded(role):
        perm_ids = RolePermission.objects.filter(role=role).values_list("permission_id", flat=True)
        permissions = Permission.objects.filter(id__in=perm_ids).values("id", "model", "action", "access_level")
        return list(permissions) 
    
    def get_action_permissions(perms, action="get"):
        return [
            {"model": perm["model"], "action": perm["action"], "access_level": perm["access_level"]}
            for perm in perms if perm["action"] == action
        ]

    def dispatch(user, model, action, access_level, data=None, pk=None):
        try:
            if not user or not user.role:
                return "Unauthorized"
            
            dispatcher_class = RolePermissionComponent.get_dispatcher(model)
            dispatcher = dispatcher_class()

            action_methods = {
                "post": dispatcher.post,
                "get": dispatcher.get,
                "put": dispatcher.put,
                "delete": dispatcher.delete,
            }
            if action in action_methods:
                method = action_methods[action]
                return method(user, model, access_level, data, pk)
            else:
                return "Invalid action"
        except Exception as err:
                raise Exception(f"Exception in dispatching action. {err}")
        
    def get_dispatcher(model):
        dispatcher_module_name = f"task_manager_app.dispatchers.{model.lower()}_dispatcher"
        try:
            dispatcher_module = importlib.import_module(dispatcher_module_name)
            dispatcher_class_name = f"{model.capitalize()}Dispatcher"
            return getattr(dispatcher_module, dispatcher_class_name, BaseDispatcher)
        except ModuleNotFoundError as err:
            print (f"[get_dispatcher] err: {err}")
            return BaseDispatcher  
        
    def handle_action(user, action_model, action, data=None, pk=None):
        perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
        specific_perms = [
            perm for perm in RolePermissionComponent.get_action_permissions(perms, action=action)
            if perm.get("model") == action_model
        ]
        if specific_perms:
            filtered_perms = specific_perms
        else:
            filtered_perms = [
                perm for perm in RolePermissionComponent.get_action_permissions(perms, action=action)
                if perm.get("model") == "_"
            ]

        result = None
        if filtered_perms:
            perm = filtered_perms[0]
            model = perm["model"]
            action = perm["action"]
            access_level = perm["access_level"]
            result = RolePermissionComponent.dispatch(user, action_model, action, access_level, data, pk)
        else:
            print(f"No matching permissions found for model: {action_model}")
            result = None

        if result is None:
            raise NotAcceptable(detail="You dont have permissions")
        elif result == "Invalid action":
            raise NotAcceptable(detail="Invalid action")
        elif result == "Unauthorized":
            raise NotAcceptable(detail="Invalid token or user not found.")
        return result
