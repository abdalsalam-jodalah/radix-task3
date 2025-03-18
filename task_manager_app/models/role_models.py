from django.db import models
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger("models")
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = '_role'

    def validate_name(self):
        if not self.name:
            raise ValidationError({"name": "Name is required."})

    def clean(self):
        super().clean()
        self.validate_name()

    def save(self, *args, **kwargs):
        self.full_clean()
        logger.debug(f"Saving Role {self.name}")
        super().save(*args, **kwargs)
