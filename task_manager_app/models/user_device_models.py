from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from .user_models import User
import logging
logger = logging.getLogger("models")

class UserDevice(models.Model):
    class Meta:
        db_table = "_user_devices"
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ['is_active']

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
 
    def validate_device_token(self):
        if not self.device_token:
            raise ValidationError({"device_token":"Empty device token"})
            self.device_token = get_random_string(64)

    def clean(self):
        super().clean()
        self.validate_device_token()

    def save(self, *args, **kwargs):
        self.full_clean()
        logger.info(f"Saving Device {self.device_name} ({self.device_type}) for user {self.user.email}")
        super().save(*args, **kwargs)
