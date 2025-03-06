from django.db import transaction
from ..models.role_models import Role
from ..models.permission_models import Permission
from ..models.role_permission_models import RolePermission

class RoleRepository:
    def get_all_roles():
        return list(Role.objects.all())  

    def get_role_by_id(role_id):
        return Role.objects.filter(pk=role_id).first()  

    def create_role(data):
        return Role.objects.create(**data) 

    def update_role(role, data):
        for key, value in data.items():
            setattr(role, key, value)
        role.save()
        return role 

    def delete_role(role):
        role.delete()
        return role  

class PermissionRepository:
    def get_all_permissions():
        return list(Permission.objects.all()) 

    def get_permission_by_id(permission_id):
        return Permission.objects.filter(pk=permission_id).first()  

    def create_permission(data):
        return Permission.objects.create(**data)  

    def update_permission(permission, data):
        for key, value in data.items():
            setattr(permission, key, value)
        permission.save()
        return permission  
    
    def delete_permission(permission):
        permission.delete()
        return permission  
    
class RolePermissionRepository:
    def get_permissions_by_role(role):
        return RolePermission.objects.filter(role=role)
    def list_role_permissions():
        return RolePermission.objects.select_related('role', 'permission').all()

    def get_role_permission(pk):
        try:
            return RolePermission.objects.select_related('role', 'permission').get(pk=pk)
        except RolePermission.DoesNotExist:
            return None

    def create_role_permission(data):
        try:
            with transaction.atomic():
                role = Role.objects.get(pk=data.get('role_id'))
                permission = Permission.objects.get(pk=data.get('permission_id'))
                rp = RolePermission.objects.create(role=role, permission=permission)
                return rp
        except Exception as e:
            raise e

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
            return None

    def delete_role_permission(pk):
        try:
            rp = RolePermission.objects.get(pk=pk)
            rp.delete()
            return True
        except RolePermission.DoesNotExist:
            return False
