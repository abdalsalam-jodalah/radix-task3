from django.db import models
from .role_models import Role
from .permission_models import Permission
import logging

logger = logging.getLogger("models")
class RolePermission(models.Model):
    id = models.AutoField(editable=False, primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = "RolePermission"
        verbose_name_plural = "RolePermissionS"
        db_table = '_role_permission'
        