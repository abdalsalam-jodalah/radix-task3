from ..repositories.role_permission_repository import RoleRepository, PermissionRepository
from ..repositories.role_permission_repository import RolePermissionRepository
from django.apps import apps
from ..dispatchers.base_dispatcher import  BaseDispatcher
import importlib
from ..models.permission_models import Permission 
from ..models.role_permission_models import RolePermission
from ..repositories.role_permission_repository import RolePermissionRepository
from rest_framework.exceptions import NotAcceptable
from rest_framework.exceptions import NotAcceptable
from rest_framework.exceptions import NotAcceptable

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

    # def get_role_permissions(role_name):
    #     """Fetch role permissions dynamically from the database."""
    #     try:
    #         role = Role.objects.prefetch_related("permissions").get(name=role_name)
    #         return set(role.permissions.values_list("name", flat=True))
    #     except Role.DoesNotExist:
    #         return set()

    def get_role_actions(user, model_name):
        if not user or not user.role:
            return {}

        permissions = RolePermissionComponent.get_permissions_by_role(user.role.name if user.role else "Guest")
        Model = apps.get_model('task_manager_app', model_name)

        return {
            "get":    lambda: Model.objects.all() if f"view_all_{model_name.lower()}" in permissions else Model.objects.filter(user=user),
            "create": lambda data: Model.objects.create(**data) if f"create_{model_name.lower()}" in permissions else None,
            "update": lambda instance, data: instance.update(**data) if f"edit_{model_name.lower()}" in permissions else None,
            "delete": lambda instance: instance.delete() if f"delete_{model_name.lower()}" in permissions else None,
        }
    

    def fetch_action_permissions(user, model_name):
        if not user or not user.role:
            return {}
        
        permissions = RolePermissionComponent.get_permissions_by_role(user.role.name if user.role else "Guest")
        Model = apps.get_model('task_manager_app', model_name)
        return {
            "get":    f"view_all_{model_name.lower()}" in permissions,
            "create": f"create_{model_name.lower()}" in permissions,
            "update": f"edit_{model_name.lower()}" in permissions,
            "delete": f"delete_{model_name.lower()}" in permissions,
        }

    def get_action_permissions_old(perms, action="get"):
        decoded = RolePermissionComponent.decode_permissions(perms)
        return [perm for perm in decoded if perm.action == action]  


    def decode_permissions(perms):
        decoded_perms = []
        print(f"++++++++++++++parts: {perms}")

        for perm in perms:
            print(f"-----------------Processing: {perm}")
            if isinstance(perm, Permission):
                decoded_perms.append(perm)
                continue  # Already a Permission object, skip further processing
            
            if not isinstance(perm, str) or not perm.strip():
                print(f"Skipping invalid permission: {repr(perm)}")  # Debugging
                continue  # Skip empty or non-string values
           
            try:
                parts = perm.split(":")
                
                if len(parts) != 3:
                    print(f"Invalid permission structure: {repr(perm)}")  # Debugging
                    continue  # Skip malformed entries
                
                model, action, access_level = parts
                print(f"parts: ")
                # Handle `_` wildcard (optional logic, depends on your system)
                if model == "_":
                    model = "global"  # You can rename `_` to a more meaningful value

                decoded_perms.append(Permission(model=model, action=action, access_level=access_level))
                print(f"Decoded -> Model: {model}, Action: {action}, Access Level: {access_level}")  # Debugging

            except Exception as e:
                print(f"Exception in decode_permissions for {repr(perm)}: {e}")
        return decoded_perms

    def get_permissions_by_role_decoded(role):
        """Fetch permissions assigned to a specific role."""
        perm_ids = RolePermission.objects.filter(role=role).values_list("permission_id", flat=True)

        permissions = Permission.objects.filter(id__in=perm_ids).values("id", "model", "action", "access_level")

        # Debugging: Print retrieved permissions
        for perm in permissions:
            print(f"ID: {perm['id']}, Model: {perm['model']}, Action: {perm['action']}, Access Level: {perm['access_level']}")
        return list(permissions) 
    
    def get_action_permissions(perms, action="get"):
        """Returns a list of permission dictionaries filtered by action."""
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
                raise Exception("Exception in dispatching action.")
        
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
