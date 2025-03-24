from rest_framework.exceptions import NotAcceptable
import importlib
import logging
from ..repositories.role_permission_repository import (
    RoleRepository,
    PermissionRepository,
    RolePermissionRepository,
)
from ..dispatchers.base_dispatcher import BaseDispatcher
from ..models.permission_models import Permission
from ..models.role_permission_models import RolePermission

logger = logging.getLogger(__name__)

class RoleComponent:
    @staticmethod
    def list_roles():
        try:
            return RoleRepository.get_all_roles()
        except Exception as e:
            logger.error(f"RoleComponent.list_roles error: {e}")
            raise Exception({"error": f"RoleComponent.list_roles error: {e}"})
    
    @staticmethod
    def get_role(role_id):
        try:
            role = RoleRepository.get_role_by_id(role_id)
            if not role:
                raise NotAcceptable(detail={"error": "Role not found."})
            return role
        except Exception as e:
            logger.error(f"RoleComponent.get_role error for role_id {role_id}: {e}")
            raise Exception({"error": f"RoleComponent.get_role error for role_id {role_id}: {e}"})
    
    @staticmethod
    def create_role(data):
        try:
            return RoleRepository.create_role(data)
        except Exception as e:
            logger.error(f"RoleComponent.create_role error: {e}")
            raise Exception({"error": f"RoleComponent.create_role error: {e}"})
    
    @staticmethod
    def update_role(role_id, data):
        try:
            role = RoleRepository.get_role_by_id(role_id)
            if role:
                return RoleRepository.update_role(role, data)
            else:
                raise NotAcceptable(detail={"error": "Role not found."})
        except Exception as e:
            logger.error(f"RoleComponent.update_role error for role_id {role_id}: {e}")
            raise Exception({"error": f"RoleComponent.update_role error for role_id {role_id}: {e}"})
    
    @staticmethod
    def delete_role(role_id):
        try:
            role = RoleRepository.get_role_by_id(role_id)
            if role:
                RoleRepository.delete_role(role)
                return True
            else:
                raise NotAcceptable(detail={"error": "Role not found."})
        except Exception as e:
            logger.error(f"RoleComponent.delete_role error for role_id {role_id}: {e}")
            raise Exception({"error": f"RoleComponent.delete_role error for role_id {role_id}: {e}"})
            

class PermissionComponent:
    @staticmethod
    def list_permissions():
        try:
            return PermissionRepository.get_all_permissions()
        except Exception as e:
            logger.error(f"PermissionComponent.list_permissions error: {e}")
            raise Exception({"error": f"PermissionComponent.list_permissions error: {e}"})
    
    @staticmethod
    def get_permission(permission_id):
        try:
            permission = PermissionRepository.get_permission_by_id(permission_id)
            if not permission:
                raise NotAcceptable(detail={"error": "Permission not found."})
            return permission
        except Exception as e:
            logger.error(f"PermissionComponent.get_permission error for permission_id {permission_id}: {e}")
            raise Exception({"error": f"PermissionComponent.get_permission error for permission_id {permission_id}: {e}"})
    
    @staticmethod
    def create_permission(data):
        try:
            return PermissionRepository.create_permission(data)
        except Exception as e:
            logger.error(f"PermissionComponent.create_permission error: {e}")
            raise Exception({"error": f"PermissionComponent.create_permission error: {e}"})
    
    @staticmethod
    def update_permission(permission_id, data):
        try:
            permission = PermissionRepository.get_permission_by_id(permission_id)
            if permission:
                return PermissionRepository.update_permission(permission, data)
            else:
                raise NotAcceptable(detail={"error": "Permission not found."})
        except Exception as e:
            logger.error(f"PermissionComponent.update_permission error for permission_id {permission_id}: {e}")
            raise Exception({"error": f"PermissionComponent.update_permission error for permission_id {permission_id}: {e}"})
    
    @staticmethod
    def delete_permission(permission_id):
        try:
            permission = PermissionRepository.get_permission_by_id(permission_id)
            if permission:
                PermissionRepository.delete_permission(permission)
                return True
            else:
                raise NotAcceptable(detail={"error": "Permission not found."})
        except Exception as e:
            logger.error(f"PermissionComponent.delete_permission error for permission_id {permission_id}: {e}")
            raise Exception({"error": f"PermissionComponent.delete_permission error for permission_id {permission_id}: {e}"})
            

class RolePermissionComponent:
    @staticmethod
    def get_permissions_by_role(role):
        try:
            return RolePermissionRepository.get_permissions_by_role(role)
        except Exception as e:
            logger.error(f"RolePermissionComponent.get_permissions_by_role error for role {role.id}: {e}")
            raise Exception({"error": f"RolePermissionComponent.get_permissions_by_role error for role {role.id}: {e}"})
    
    @staticmethod
    def list_role_permissions():
        try:
            return RolePermissionRepository.list_role_permissions()
        except Exception as e:
            logger.error(f"RolePermissionComponent.list_role_permissions error: {e}")
            raise Exception({"error": f"RolePermissionComponent.list_role_permissions error: {e}"})
    
    @staticmethod
    def get_role_permission(pk):
        try:
            role_permission = RolePermissionRepository.get_role_permission(pk)
            if not role_permission:
                raise NotAcceptable(detail={"error": "RolePermission not found."})
            return role_permission
        except Exception as e:
            logger.error(f"RolePermissionComponent.get_role_permission error for pk {pk}: {e}")
            raise Exception({"error": f"RolePermissionComponent.get_role_permission error for pk {pk}: {e}"})
    
    @staticmethod
    def create_role_permission(data):
        try:
            return RolePermissionRepository.create_role_permission(data)
        except Exception as e:
            logger.error(f"RolePermissionComponent.create_role_permission error: {e}")
            raise Exception({"error": f"RolePermissionComponent.create_role_permission error: {e}"})
    
    @staticmethod
    def update_role_permission(pk, data):
        try:
            rp = RolePermissionRepository.update_role_permission(pk, data)
            if not rp:
                raise NotAcceptable(detail={"error": "RolePermission not found."})
            return rp
        except Exception as e:
            logger.error(f"RolePermissionComponent.update_role_permission error for pk {pk}: {e}")
            raise Exception({"error": f"RolePermissionComponent.update_role_permission error for pk {pk}: {e}"})
    
    @staticmethod
    def delete_role_permission(pk):
        try:
            result = RolePermissionRepository.delete_role_permission(pk)
            if not result:
                raise NotAcceptable(detail={"error": "RolePermission not found."})
            return True
        except Exception as e:
            logger.error(f"RolePermissionComponent.delete_role_permission error for pk {pk}: {e}")
            raise Exception({"error": f"RolePermissionComponent.delete_role_permission error for pk {pk}: {e}"})
    
    @staticmethod
    def get_permissions_by_role_decoded(role):
        try:
            perm_ids = RolePermission.objects.filter(role=role).values_list("permission_id", flat=True)
            permissions = Permission.objects.filter(id__in=perm_ids).values("id", "model", "action", "access_level")
            return list(permissions)
        except Exception as e:
            logger.error(f"RolePermissionComponent.get_permissions_by_role_decoded error for role {role.id}: {e}")
            raise Exception({"error": f"RolePermissionComponent.get_permissions_by_role_decoded error for role {role.id}: {e}"})
    
    @staticmethod
    def get_action_permissions(perms, action="get"):
        try:
            return [
                {"model": perm["model"], "action": perm["action"], "access_level": perm["access_level"]}
                for perm in perms if perm["action"] == action
            ]
        except Exception as e:
            logger.error(f"RolePermissionComponent.get_action_permissions error for action {action}: {e}")
            raise Exception({"error": f"RolePermissionComponent.get_action_permissions error for action {action}: {e}"})
    
    @staticmethod
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
            logger.error(f"RolePermissionComponent.dispatch error: {err}")
            raise err
    
    @staticmethod
    def get_dispatcher(model):
        dispatcher_module_name = f"task_manager_app.dispatchers.{model.lower()}_dispatcher"
        try:
            dispatcher_module = importlib.import_module(dispatcher_module_name)
            dispatcher_class_name = f"{model.capitalize()}Dispatcher"
            return getattr(dispatcher_module, dispatcher_class_name, BaseDispatcher)
        except ModuleNotFoundError as err:
            logger.error(f"RolePermissionComponent.get_dispatcher module not found: {err}")
            return BaseDispatcher
    
    @staticmethod
    def handle_action(user, action_model, action, data=None, pk=None):
     
        perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
        specific_perms = [
            perm for perm in RolePermissionComponent.get_action_permissions(perms, action=action)
            if perm.get("model") == action_model
        ]
        filtered_perms = specific_perms if specific_perms else [
            perm for perm in RolePermissionComponent.get_action_permissions(perms, action=action)
            if perm.get("model") == "_"
        ]
        result = None
        print(filtered_perms)
        if filtered_perms:
            perm = filtered_perms[0]
            model_name = perm["model"]
            action_name = perm["action"]
            access_level = perm["access_level"]
            result = RolePermissionComponent.dispatch(user, action_model, action_name, access_level, data, pk)
        else:
            logger.info(f"No matching permissions found for model: {action_model}")
            result = None
        
        if result is None:
            raise NotAcceptable(detail={"error": "You don't have permissions"})
        elif result == "Invalid action":
            raise NotAcceptable(detail={"error": "Invalid action"})
        elif result == "Unauthorized":
            raise NotAcceptable(detail={"error": "Invalid token or user not found."})
        return result
    