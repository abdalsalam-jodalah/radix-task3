from django.db import models
import logging

logger = logging.getLogger("models")
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    model= models.CharField(max_length=50, blank=True, null=True)
    action= models.CharField(max_length=50, blank=True, null=True)
    access_level = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ManyToManyField("Role", related_name="permission")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        db_table = '_permission'
        