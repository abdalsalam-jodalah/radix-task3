from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password  
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

from .user_models import User

import logging

logger = logging.getLogger("models")

class UserDevice(models.Model):
    class Meta:
        db_table = "_user_devices"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    is_active = models.BooleanField(default=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    device_name = models.CharField(max_length=255, blank=True, default="Unknown Device")
    device_type = models.CharField(max_length=100, default="Unknown Type")
    device_token = models.CharField(
        max_length=255, 
        unique=True, 
        default=get_random_string(64)  
    )

    def __str__(self):
        return f"{self.device_name} - {self.device_type} ({'Active' if self.is_active else 'Inactive'})"

    def clean(self):
        """Custom validation for device token."""
        if not self.device_token or len(self.device_token) < 20:
            raise ValidationError("Invalid device token. Must be at least 20 characters long.")

    def save(self, *args, **kwargs):
        """Custom save method with logging and security improvements."""
        if not self.device_token:
            self.device_token = get_random_string(64)

        logger.info(f"Saving device {self.device_name} ({self.device_type}) for user {self.user.email}")
        super().save(*args, **kwargs)
